CREATE TABLE customers (
    customer_id BIGINT GENERATED ALWAYS AS IDENTITY,
    name        VARCHAR(150) NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20),

    status      VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at  TIMESTAMPTZ,

    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_customers
        PRIMARY KEY (customer_id),

    CONSTRAINT chk_customers_name
        CHECK (BTRIM(name) <> ''),

    CONSTRAINT chk_customers_status
        CHECK (
            status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED')
        ),

    CONSTRAINT chk_customers_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);

CREATE UNIQUE INDEX uq_customers_email_ci
    ON customers (LOWER(email))
    WHERE deleted_at IS NULL;