CREATE TABLE metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE followers (
    actor_url TEXT PRIMARY KEY,
    inbox_url TEXT NOT NULL,
    shared_inbox_url TEXT,
    follow_id TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE posts (
    source_id TEXT PRIMARY KEY,
    object_url TEXT NOT NULL UNIQUE,
    activity_url TEXT,
    content_hash TEXT NOT NULL,
    published TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN (
        'historical', 'pending', 'delivered', 'cancelled', 'redacted'
    )),
    deleted_at TEXT
);

CREATE TABLE replies (
    activity_id TEXT PRIMARY KEY,
    object_url TEXT NOT NULL,
    actor_url TEXT NOT NULL,
    source_id TEXT NOT NULL,
    received_at TEXT NOT NULL
);
CREATE INDEX replies_source_id ON replies(source_id, received_at);

CREATE TABLE interactions (
    activity_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('Like', 'Announce')),
    actor_url TEXT NOT NULL,
    source_id TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    received_at TEXT NOT NULL,
    UNIQUE (kind, actor_url, source_id)
);
CREATE INDEX interactions_source_id ON interactions(source_id, kind, active);

CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    destination TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('Create', 'Delete', 'Accept')),
    activity_id TEXT NOT NULL,
    body TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'delivered', 'failed')),
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt TEXT NOT NULL,
    last_error TEXT,
    UNIQUE (source_id, destination, kind)
);
CREATE INDEX deliveries_due ON deliveries(status, next_attempt);

CREATE TABLE delivery_recipients (
    source_id TEXT NOT NULL,
    destination TEXT NOT NULL,
    PRIMARY KEY (source_id, destination)
);
