CREATE TABLE refunds (
    refund_id     BIGINT GENERATED ALWAYS AS IDENTITY,

    payment_id    BIGINT NOT NULL,
    return_id     BIGINT,

    amount        NUMERIC(12,2) NOT NULL,

    status        VARCHAR(25) NOT NULL DEFAULT 'REQUESTED',

    requested_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at  TIMESTAMPTZ,

    created_at    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_refunds
        PRIMARY KEY (refund_id),

    CONSTRAINT fk_refunds_payment
        FOREIGN KEY (payment_id)
        REFERENCES payments (payment_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_refunds_return
        FOREIGN KEY (return_id)
        REFERENCES returns (return_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_refunds_amount
        CHECK (amount > 0),

    CONSTRAINT chk_refunds_status
        CHECK (
            status IN (
                'REQUESTED',
                'PROCESSING',
                'COMPLETED',
                'FAILED',
                'CANCELLED'
            )
        )
);

CREATE INDEX idx_refunds_payment_id
    ON refunds (payment_id);

CREATE INDEX idx_refunds_return_id
    ON refunds (return_id);

CREATE INDEX idx_refunds_status
    ON refunds (status);