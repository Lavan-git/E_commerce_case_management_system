CREATE TABLE products (
    product_id  BIGINT GENERATED ALWAYS AS IDENTITY,
    name        VARCHAR(200) NOT NULL,
    description TEXT,

    status      VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at  TIMESTAMPTZ,

    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_products
        PRIMARY KEY (product_id),

    CONSTRAINT chk_products_name
        CHECK (BTRIM(name) <> ''),

    CONSTRAINT chk_products_status
        CHECK (
            status IN (
                'ACTIVE',
                'INACTIVE',
                'DISCONTINUED'
            )
        ),

    CONSTRAINT chk_products_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);