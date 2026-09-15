CREATE TABLE order_items (
    order_item_id      BIGINT GENERATED ALWAYS AS IDENTITY,
    order_id           BIGINT NOT NULL,
    vendor_product_id  BIGINT NOT NULL,

    quantity            INTEGER NOT NULL,
    unit_price          NUMERIC(12,2) NOT NULL,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_order_items
        PRIMARY KEY (order_item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_order_items_vendor_product
        FOREIGN KEY (vendor_product_id)
        REFERENCES vendor_products (vendor_product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_order_items_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_items_unit_price
        CHECK (unit_price >= 0)
);

CREATE INDEX idx_order_items_order_id
    ON order_items (order_id);

CREATE INDEX idx_order_items_vendor_product_id
    ON order_items (vendor_product_id);