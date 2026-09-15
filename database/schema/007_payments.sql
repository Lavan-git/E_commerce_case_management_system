CREATE TABLE payments (
    payment_id            BIGINT GENERATED ALWAYS AS IDENTITY,
    customer_id           BIGINT NOT NULL,
    order_id              BIGINT,

    transaction_reference VARCHAR(100),

    amount                NUMERIC(12,2) NOT NULL,
    payment_method        VARCHAR(30) NOT NULL,

    status                VARCHAR(25) NOT NULL DEFAULT 'PENDING',

    transaction_time      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_payments
        PRIMARY KEY (payment_id),

    CONSTRAINT fk_payments_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_payments_amount
        CHECK (amount > 0),

    CONSTRAINT chk_payments_method
        CHECK (
            payment_method IN (
                'CARD',
                'UPI',
                'NET_BANKING',
                'WALLET',
                'COD',
                'OTHER'
            )
        ),

    CONSTRAINT chk_payments_status
        CHECK (
            status IN (
                'PENDING',
                'SUCCESS',
                'FAILED',
                'CANCELLED',
                'REFUNDED',
                'PARTIALLY_REFUNDED'
            )
        )
);

CREATE UNIQUE INDEX uq_payments_transaction_reference
    ON payments (transaction_reference)
    WHERE transaction_reference IS NOT NULL;

CREATE INDEX idx_payments_customer_id
    ON payments (customer_id);

CREATE INDEX idx_payments_order_id
    ON payments (order_id);

CREATE INDEX idx_payments_transaction_time
    ON payments (transaction_time);