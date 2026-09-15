CREATE TABLE delivery_persons (
    delivery_person_id BIGINT GENERATED ALWAYS AS IDENTITY,

    name               VARCHAR(150) NOT NULL,
    phone              VARCHAR(20),

    status             VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at         TIMESTAMPTZ,

    created_at         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_delivery_persons
        PRIMARY KEY (delivery_person_id),

    CONSTRAINT chk_delivery_persons_name
        CHECK (BTRIM(name) <> ''),

    CONSTRAINT chk_delivery_persons_status
        CHECK (
            status IN (
                'ACTIVE',
                'INACTIVE',
                'SUSPENDED'
            )
        ),

    CONSTRAINT chk_delivery_persons_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);