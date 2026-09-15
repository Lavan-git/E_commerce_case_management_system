CREATE TABLE vendor_products (
    vendor_product_id BIGINT GENERATED ALWAYS AS IDENTITY,
    vendor_id         BIGINT NOT NULL,
    product_id        BIGINT NOT NULL,

    price             NUMERIC(12,2) NOT NULL,

    status            VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at        TIMESTAMPTZ,

    created_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_vendor_products
        PRIMARY KEY (vendor_product_id),

    CONSTRAINT fk_vendor_products_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors (vendor_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_vendor_products_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_vendor_products_price
        CHECK (price >= 0),

    CONSTRAINT chk_vendor_products_status
        CHECK (
            status IN (
                'ACTIVE',
                'INACTIVE',
                'OUT_OF_STOCK',
                'DISCONTINUED'
            )
        ),

    CONSTRAINT chk_vendor_products_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);

CREATE UNIQUE INDEX uq_vendor_products_active_listing
    ON vendor_products (vendor_id, product_id)
    WHERE deleted_at IS NULL;