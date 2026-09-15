CREATE TABLE vendor_payouts (
    payout_id            BIGINT GENERATED ALWAYS AS IDENTITY,
    vendor_id            BIGINT NOT NULL,

    expected_amount      NUMERIC(12,2) NOT NULL,
    actual_amount        NUMERIC(12,2),

    expected_payout_date DATE,
    paid_at              TIMESTAMPTZ,

    status               VARCHAR(25) NOT NULL DEFAULT 'PENDING',

    created_at            TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_vendor_payouts
        PRIMARY KEY (payout_id),

    CONSTRAINT fk_vendor_payouts_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES vendors (vendor_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_vendor_payouts_expected_amount
        CHECK (expected_amount >= 0),

    CONSTRAINT chk_vendor_payouts_actual_amount
        CHECK (
            actual_amount IS NULL
            OR actual_amount >= 0
        ),

    CONSTRAINT chk_vendor_payouts_status
        CHECK (
            status IN (
                'PENDING',
                'PROCESSING',
                'PAID',
                'FAILED',
                'ON_HOLD',
                'CANCELLED'
            )
        )
);

CREATE INDEX idx_vendor_payouts_vendor_id
    ON vendor_payouts (vendor_id);

CREATE INDEX idx_vendor_payouts_status
    ON vendor_payouts (status);

CREATE INDEX idx_vendor_payouts_expected_date
    ON vendor_payouts (expected_payout_date);