CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE models (
model_id TEXT PRIMARY KEY,
pipeline_tag TEXT,
library_name TEXT,
author TEXT,
downloads INT DEFAULT 0,
likes INT DEFAULT 0,
last_modified TIMESTAMPTZ,
private BOOLEAN,
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE model_tags (
    model_id TEXT REFERENCES models(model_id) ON DELETE CASCADE,
    tag TEXT,
    PRIMARY KEY (model_id, tag)
);

CREATE TABLE model_snapshots (
    id SERIAL PRIMARY KEY,
    model_id TEXT REFERENCES models(model_id) ON DELETE CASCADE,
    downloads INT DEFAULT 0,
    likes INT DEFAULT 0,
    snapshot_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE model_meta (
    model_id TEXT PRIMARY KEY REFERENCES models(model_id) ON DELETE CASCADE,
    config JSONB,
    card_data JSONB 
);

CREATE TABLE pipeline_log (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT NOW(),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    fetched_count INT,
    inserted_count INT,
    updated_count INT,
    error_count INT,
    log_message TEXT
);