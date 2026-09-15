CREATE TABLE delivery_attempts (
    attempt_id          BIGINT GENERATED ALWAYS AS IDENTITY,

    delivery_id         BIGINT NOT NULL,
    delivery_person_id  BIGINT,

    attempted_at        TIMESTAMPTZ NOT NULL,

    status              VARCHAR(20) NOT NULL,
    failure_reason      VARCHAR(255),
    remarks             TEXT,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_delivery_attempts
        PRIMARY KEY (attempt_id),

    CONSTRAINT fk_delivery_attempts_delivery
        FOREIGN KEY (delivery_id)
        REFERENCES deliveries (delivery_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_delivery_attempts_person
        FOREIGN KEY (delivery_person_id)
        REFERENCES delivery_persons (delivery_person_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_delivery_attempts_status
        CHECK (
            status IN (
                'SUCCESS',
                'FAILED'
            )
        ),

    CONSTRAINT chk_delivery_attempts_failure_reason
        CHECK (
            status = 'SUCCESS'
            OR failure_reason IS NOT NULL
        )
);

CREATE INDEX idx_delivery_attempts_delivery_id
    ON delivery_attempts (delivery_id);

CREATE INDEX idx_delivery_attempts_attempted_at
    ON delivery_attempts (attempted_at);