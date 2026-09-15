CREATE TABLE case_updates (
    update_id           BIGINT GENERATED ALWAYS AS IDENTITY,

    case_id             BIGINT NOT NULL,
    updated_by_agent_id BIGINT,

    source              VARCHAR(20) NOT NULL DEFAULT 'AGENT',

    old_status          VARCHAR(25),
    new_status          VARCHAR(25),

    comment             TEXT NOT NULL,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_case_updates
        PRIMARY KEY (update_id),

    CONSTRAINT fk_case_updates_case
        FOREIGN KEY (case_id)
        REFERENCES cases (case_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_case_updates_agent
        FOREIGN KEY (updated_by_agent_id)
        REFERENCES support_agents (agent_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_case_updates_source
        CHECK (
            source IN (
                'AGENT',
                'SYSTEM',
                'AI'
            )
        ),

    CONSTRAINT chk_case_updates_agent_required
        CHECK (
            source <> 'AGENT'
            OR updated_by_agent_id IS NOT NULL
        ),

    CONSTRAINT chk_case_updates_comment
        CHECK (BTRIM(comment) <> '')
);

CREATE INDEX idx_case_updates_case_id
    ON case_updates (case_id);

CREATE INDEX idx_case_updates_agent_id
    ON case_updates (updated_by_agent_id);

CREATE INDEX idx_case_updates_created_at
    ON case_updates (created_at);