CREATE TABLE deliveries (
    delivery_id          BIGINT GENERATED ALWAYS AS IDENTITY,

    order_id             BIGINT NOT NULL,
    delivery_person_id   BIGINT,

    delivery_partner     VARCHAR(100),
    tracking_number      VARCHAR(100),

    status               VARCHAR(25) NOT NULL DEFAULT 'ASSIGNED',

    shipped_at           TIMESTAMPTZ,
    expected_delivery_at TIMESTAMPTZ,
    delivered_at         TIMESTAMPTZ,

    created_at            TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_deliveries
        PRIMARY KEY (delivery_id),

    CONSTRAINT fk_deliveries_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_deliveries_person
        FOREIGN KEY (delivery_person_id)
        REFERENCES delivery_persons (delivery_person_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_deliveries_status
        CHECK (
            status IN (
                'CREATED',
                'ASSIGNED',
                'PICKED_UP',
                'IN_TRANSIT',
                'OUT_FOR_DELIVERY',
                'DELIVERED',
                'FAILED',
                'LOST',
                'CANCELLED'
            )
        )
);

CREATE UNIQUE INDEX uq_deliveries_tracking_number
    ON deliveries (tracking_number)
    WHERE tracking_number IS NOT NULL;

CREATE INDEX idx_deliveries_order_id
    ON deliveries (order_id);

CREATE INDEX idx_deliveries_delivery_person_id
    ON deliveries (delivery_person_id);

CREATE INDEX idx_deliveries_status
    ON deliveries (status);