CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id UUID PRIMARY KEY,

    source_name VARCHAR(50) NOT NULL,
    batch_id VARCHAR(100) NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),

    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,

    source_count INTEGER NOT NULL DEFAULT 0
        CHECK (source_count >= 0),

    standardized_count INTEGER NOT NULL DEFAULT 0
        CHECK (standardized_count >= 0),

    rejected_count INTEGER NOT NULL DEFAULT 0
        CHECK (rejected_count >= 0),

    already_present_count INTEGER NOT NULL DEFAULT 0
        CHECK (already_present_count >= 0),

    persisted_count INTEGER NOT NULL DEFAULT 0
        CHECK (persisted_count >= 0),

    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_source_batch
    ON pipeline_runs (source_name, batch_id);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status
    ON pipeline_runs (status);