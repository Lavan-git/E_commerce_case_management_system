CREATE TABLE returns (
    return_id      BIGINT GENERATED ALWAYS AS IDENTITY,

    order_item_id  BIGINT NOT NULL,

    reason         VARCHAR(255) NOT NULL,
    status         VARCHAR(25) NOT NULL DEFAULT 'REQUESTED',

    requested_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    picked_up_at   TIMESTAMPTZ,
    completed_at   TIMESTAMPTZ,

    created_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_returns
        PRIMARY KEY (return_id),

    CONSTRAINT fk_returns_order_item
        FOREIGN KEY (order_item_id)
        REFERENCES order_items (order_item_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_returns_reason
        CHECK (BTRIM(reason) <> ''),

    CONSTRAINT chk_returns_status
        CHECK (
            status IN (
                'REQUESTED',
                'APPROVED',
                'REJECTED',
                'PICKED_UP',
                'RECEIVED',
                'COMPLETED',
                'CANCELLED'
            )
        )
);

CREATE INDEX idx_returns_order_item_id
    ON returns (order_item_id);

CREATE INDEX idx_returns_status
    ON returns (status);