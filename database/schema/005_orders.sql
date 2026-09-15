CREATE TABLE orders (
    order_id     BIGINT GENERATED ALWAYS AS IDENTITY,
    customer_id  BIGINT NOT NULL,

    ordered_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(12,2) NOT NULL,

    status       VARCHAR(25) NOT NULL DEFAULT 'PLACED',

    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_orders
        PRIMARY KEY (order_id),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_orders_total_amount
        CHECK (total_amount >= 0),

    CONSTRAINT chk_orders_status
        CHECK (
            status IN (
                'PLACED',
                'CONFIRMED',
                'PROCESSING',
                'SHIPPED',
                'OUT_FOR_DELIVERY',
                'DELIVERED',
                'CANCELLED',
                'FAILED'
            )
        )
);

CREATE INDEX idx_orders_customer_id
    ON orders (customer_id);

CREATE INDEX idx_orders_ordered_at
    ON orders (ordered_at);