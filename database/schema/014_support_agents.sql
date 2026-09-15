CREATE TABLE support_agents (
    agent_id     BIGINT GENERATED ALWAYS AS IDENTITY,

    name         VARCHAR(150) NOT NULL,
    email        VARCHAR(254) NOT NULL,

    status       VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at   TIMESTAMPTZ,

    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_support_agents
        PRIMARY KEY (agent_id),

    CONSTRAINT chk_support_agents_name
        CHECK (BTRIM(name) <> ''),

    CONSTRAINT chk_support_agents_status
        CHECK (
            status IN (
                'ACTIVE',
                'INACTIVE',
                'SUSPENDED'
            )
        ),

    CONSTRAINT chk_support_agents_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);

CREATE UNIQUE INDEX uq_support_agents_email_ci
    ON support_agents (LOWER(email))
    WHERE deleted_at IS NULL;