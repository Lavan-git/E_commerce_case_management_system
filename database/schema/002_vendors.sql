CREATE TABLE vendors (
    vendor_id      BIGINT GENERATED ALWAYS AS IDENTITY,
    business_name  VARCHAR(200) NOT NULL,
    legal_name     VARCHAR(200),
    email          VARCHAR(254) NOT NULL,
    phone          VARCHAR(20),
    gstin          VARCHAR(15),
    pan            VARCHAR(10),

    kyc_status     VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    status         VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    deleted_at     TIMESTAMPTZ,

    created_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_vendors
        PRIMARY KEY (vendor_id),

    CONSTRAINT chk_vendors_business_name
        CHECK (BTRIM(business_name) <> ''),

    CONSTRAINT chk_vendors_kyc_status
        CHECK (
            kyc_status IN (
                'PENDING',
                'VERIFIED',
                'REJECTED'
            )
        ),

    CONSTRAINT chk_vendors_status
        CHECK (
            status IN (
                'ACTIVE',
                'INACTIVE',
                'SUSPENDED'
            )
        ),

    CONSTRAINT chk_vendors_deleted_status
        CHECK (
            deleted_at IS NULL
            OR status = 'INACTIVE'
        )
);

CREATE UNIQUE INDEX uq_vendors_email_ci
    ON vendors (LOWER(email))
    WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX uq_vendors_gstin
    ON vendors (gstin)
    WHERE gstin IS NOT NULL
      AND deleted_at IS NULL;

CREATE UNIQUE INDEX uq_vendors_pan
    ON vendors (pan)
    WHERE pan IS NOT NULL
      AND deleted_at IS NULL;