from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from email.utils import format_datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar

import pytest

from activitypub.worker.core import PUBLIC
from activitypub.worker.core import digest_header
from activitypub.worker.core import signature_header
from activitypub.worker.core import signature_input


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _pywrangler() -> Path | None:
    configured = os.environ.get("PYWRANGLER")
    if configured:
        return Path(configured)
    installed = shutil.which("pywrangler")
    if installed:
        return Path(installed)
    candidate = Path(__file__).resolve().parents[1] / "activitypub/.venv/bin/pywrangler"
    return candidate if candidate.exists() else None


class _FederationHandler(BaseHTTPRequestHandler):
    base_url = ""
    public_key = ""
    manifest: ClassVar[dict] = {"version": 1, "actor": "", "posts": []}
    notes: ClassVar[dict[str, dict]] = {}
    inbox: ClassVar[list[dict]] = []

    def log_message(self, _format, *_args):
        return

    def _send_json(
        self, value: object, status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/activity+json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urllib.parse.urlsplit(self.path).path.rstrip("/")
        if path == "/users/remote":
            actor = f"{self.base_url}/users/remote"
            self._send_json(
                {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "id": actor,
                    "type": "Person",
                    "inbox": f"{self.base_url}/inbox",
                    "endpoints": {"sharedInbox": f"{self.base_url}/inbox"},
                    "publicKey": {
                        "id": f"{actor}#main-key",
                        "owner": actor,
                        "publicKeyPem": self.public_key,
                    },
                }
            )
        elif path == "/activitypub/manifest.json":
            self._send_json(self.manifest)
        elif path.startswith("/activitypub/posts/"):
            note = self.notes.get(path)
            self._send_json(
                note or {"error": "not found"},
                HTTPStatus.OK if note else HTTPStatus.NOT_FOUND,
            )
        else:
            self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.inbox.append(json.loads(body))
        self._send_json({"ok": True}, HTTPStatus.ACCEPTED)


class _WorkerHarness:
    """Running workerd, local D1, and a fake remote ActivityPub server."""

    def __init__(self, pywrangler: Path) -> None:
        self.repo = Path(__file__).resolve().parents[1]
        self.temporary = tempfile.TemporaryDirectory()
        self.worker_root = Path(self.temporary.name) / "activitypub"
        shutil.copytree(
            self.repo / "activitypub",
            self.worker_root,
            ignore=shutil.ignore_patterns(
                ".venv", ".venv-workers", ".wrangler", "__pycache__"
            ),
        )
        private_key = (self.repo / "activitypub/private-key.pem").read_text()
        public_key = (self.repo / "activitypub/public-key.pem").read_text()

        self.remote_port = _free_port()
        self.worker_port = _free_port()
        self.remote_base = f"http://127.0.0.1:{self.remote_port}"
        self.worker_base = f"http://127.0.0.1:{self.worker_port}"
        _FederationHandler.base_url = self.remote_base
        _FederationHandler.public_key = public_key
        _FederationHandler.manifest = {
            "version": 1,
            "actor": f"{self.remote_base}/activitypub/wrlach",
            "posts": [],
        }
        _FederationHandler.notes = {}
        _FederationHandler.inbox = []
        self.remote = ThreadingHTTPServer(
            ("127.0.0.1", self.remote_port), _FederationHandler
        )
        self.remote_thread = threading.Thread(
            target=self.remote.serve_forever, daemon=True
        )
        self.remote_thread.start()

        config_path = self.worker_root / "wrangler.toml"
        config = config_path.read_text()
        config = config.replace("https://wrla.ch", self.remote_base)
        config = config.replace(
            'ALLOW_INSECURE_TEST_URLS = "false"',
            'ALLOW_INSECURE_TEST_URLS = "true"',
        )
        config = config.replace(
            'OUTBOUND_DELIVERY_ENABLED = "false"',
            'OUTBOUND_DELIVERY_ENABLED = "true"',
        )
        config = config.replace(
            "REPLACE_WITH_D1_DATABASE_ID",
            "00000000-0000-0000-0000-000000000000",
        )
        config = config.split("[[routes]]", 1)[0]
        config_path.write_text(config)
        escaped_key = private_key.replace('"', '\\"')
        (self.worker_root / ".dev.vars").write_text(
            f'ACTIVITYPUB_PRIVATE_KEY="{escaped_key}"\n'
        )

        command = str(pywrangler)
        migration = subprocess.run(
            [
                command,
                "d1",
                "migrations",
                "apply",
                "wrla-ch-activitypub",
                "--local",
            ],
            cwd=self.worker_root,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if migration.returncode:
            raise RuntimeError(
                f"D1 migration failed:\n{migration.stdout}\n{migration.stderr}"
            )
        self.worker = subprocess.Popen(
            [command, "dev", "--ip", "127.0.0.1", "--port", str(self.worker_port)],
            cwd=self.worker_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(
                    f"{self.worker_base}/.well-known/webfinger?resource="
                    "acct%3Awrlach%40127.0.0.1",
                    timeout=1,
                ):
                    break
            except (urllib.error.URLError, TimeoutError):
                if self.worker.poll() is not None:
                    output = self.worker.stdout.read() if self.worker.stdout else ""
                    raise RuntimeError(f"pywrangler exited early:\n{output}") from None
                time.sleep(0.25)
        else:
            raise RuntimeError("Timed out waiting for pywrangler")
        self.private_key_path = self.repo / "activitypub/private-key.pem"

    def close(self) -> None:
        self.worker.terminate()
        try:
            self.worker.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.worker.kill()
        self.remote.shutdown()
        self.remote.server_close()
        self.temporary.cleanup()

    def request(
        self, path: str, *, method: str = "GET", value: dict | None = None
    ) -> tuple[int, dict | None]:
        data = json.dumps(value, separators=(",", ":")).encode() if value else None
        headers: dict[str, str] = {}
        if data is not None:
            date = format_datetime(datetime.now(UTC), usegmt=True)
            digest = digest_header(data)
            url = f"{self.worker_base}{path}"
            signed = signature_input(
                method=method,
                url=url,
                headers={"date": date, "digest": digest},
                covered=("(request-target)", "host", "date", "digest"),
            )
            signature = subprocess.run(
                ["openssl", "dgst", "-sha256", "-sign", str(self.private_key_path)],
                input=signed,
                capture_output=True,
                check=True,
            ).stdout
            headers = {
                "Content-Type": "application/activity+json",
                "Date": date,
                "Digest": digest,
                "Signature": signature_header(
                    f"{self.remote_base}/users/remote#main-key", signature
                ),
            }
        request = urllib.request.Request(
            f"{self.worker_base}{path}", data=data, headers=headers, method=method
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None

    def schedule(self, when: datetime) -> None:
        encoded = urllib.parse.quote(when.isoformat().replace("+00:00", "Z"))
        status, _ = self.request(f"/__test/scheduled?time={encoded}", method="POST")
        assert status == HTTPStatus.OK


@pytest.fixture(scope="module")
def worker_harness() -> _WorkerHarness:
    pywrangler = _pywrangler()
    if pywrangler is None:
        pytest.skip("pywrangler is not installed")
    harness = _WorkerHarness(pywrangler)
    try:
        yield harness
    finally:
        harness.close()


def test_federation_lifecycle(worker_harness: _WorkerHarness) -> None:
    remote_actor = f"{worker_harness.remote_base}/users/remote"
    local_actor = f"{worker_harness.remote_base}/activitypub/wrlach"
    follow = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"{remote_actor}/follows/1",
        "type": "Follow",
        "actor": remote_actor,
        "object": local_actor,
    }
    status, _ = worker_harness.request(
        "/activitypub/wrlach/inbox", method="POST", value=follow
    )
    assert status == HTTPStatus.ACCEPTED
    assert _FederationHandler.inbox[-1]["type"] == "Accept"

    observed = datetime.now(UTC).replace(microsecond=0)
    worker_harness.schedule(observed)
    source_id = "20260824000000-integration-post"
    object_url = f"{worker_harness.remote_base}/activitypub/posts/{source_id}"
    note = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": object_url,
        "type": "Note",
        "attributedTo": local_actor,
        "published": "2026-08-24T00:00:00Z",
        "content": "<p>Integration test.</p>",
        "to": [PUBLIC],
        "cc": [f"{local_actor}/followers"],
    }
    _FederationHandler.notes[f"/activitypub/posts/{source_id}"] = note
    _FederationHandler.manifest["posts"] = [
        {
            "source_id": source_id,
            "published": note["published"],
            "object": object_url,
            "activity": f"{object_url}/activity",
            "content_hash": "a" * 64,
            "redacted": False,
        }
    ]
    worker_harness.schedule(observed)
    assert not any(item["type"] == "Create" for item in _FederationHandler.inbox)
    worker_harness.schedule(observed + timedelta(minutes=16))
    assert _FederationHandler.inbox[-1]["type"] == "Create"

    like = {
        "id": f"{remote_actor}/likes/1",
        "type": "Like",
        "actor": remote_actor,
        "object": object_url,
    }
    worker_harness.request("/activitypub/wrlach/inbox", method="POST", value=like)
    _, likes = worker_harness.request(f"/activitypub/likes/{source_id}")
    assert likes is not None
    assert likes["totalItems"] == 1

    reply = {
        "id": f"{remote_actor}/activities/reply-1",
        "type": "Create",
        "actor": remote_actor,
        "object": {
            "id": f"{remote_actor}/notes/reply-1",
            "type": "Note",
            "attributedTo": remote_actor,
            "inReplyTo": object_url,
            "to": [PUBLIC],
        },
    }
    worker_harness.request("/activitypub/wrlach/inbox", method="POST", value=reply)
    _, collection = worker_harness.request(f"/activitypub/replies/{source_id}")
    assert collection is not None
    assert collection["totalItems"] == 1
    _, replies = worker_harness.request(f"/activitypub/replies/{source_id}?page=1")
    assert replies is not None
    assert replies["orderedItems"] == [reply["object"]["id"]]

    _FederationHandler.manifest["posts"][0].update(
        {"redacted": True, "deleted": "2026-08-24T01:00:00Z"}
    )
    worker_harness.schedule(observed + timedelta(minutes=17))
    assert _FederationHandler.inbox[-1]["type"] == "Delete"
