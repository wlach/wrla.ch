CREATE TABLE quote_authorizations (
    authorization_id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    actor_url TEXT NOT NULL,
    quote_url TEXT NOT NULL,
    target_url TEXT NOT NULL,
    source_id TEXT NOT NULL,
    received_at TEXT NOT NULL,
    UNIQUE (actor_url, quote_url, target_url)
);
CREATE INDEX quote_authorizations_source_id
    ON quote_authorizations(source_id, received_at);
