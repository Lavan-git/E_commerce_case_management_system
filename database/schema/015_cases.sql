CREATE TABLE cases (
    case_id                BIGINT GENERATED ALWAYS AS IDENTITY,

    raised_by_customer_id  BIGINT,
    raised_by_vendor_id    BIGINT,

    case_type              VARCHAR(30) NOT NULL,
    category               VARCHAR(50) NOT NULL,
    reason                 VARCHAR(255) NOT NULL,
    description            TEXT NOT NULL,

    priority               VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    status                 VARCHAR(25) NOT NULL DEFAULT 'OPEN',

    assigned_agent_id      BIGINT,

    order_id               BIGINT,
    order_item_id          BIGINT,
    payment_id             BIGINT,
    delivery_id            BIGINT,
    return_id              BIGINT,
    refund_id              BIGINT,
    vendor_payout_id       BIGINT,

    resolution             TEXT,

    created_at             TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at            TIMESTAMPTZ,

    CONSTRAINT pk_cases
        PRIMARY KEY (case_id),

    CONSTRAINT fk_cases_customer
        FOREIGN KEY (raised_by_customer_id)
        REFERENCES customers (customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_vendor
        FOREIGN KEY (raised_by_vendor_id)
        REFERENCES vendors (vendor_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_agent
        FOREIGN KEY (assigned_agent_id)
        REFERENCES support_agents (agent_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_order
        FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_order_item
        FOREIGN KEY (order_item_id)
        REFERENCES order_items (order_item_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_payment
        FOREIGN KEY (payment_id)
        REFERENCES payments (payment_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_delivery
        FOREIGN KEY (delivery_id)
        REFERENCES deliveries (delivery_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_return
        FOREIGN KEY (return_id)
        REFERENCES returns (return_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_refund
        FOREIGN KEY (refund_id)
        REFERENCES refunds (refund_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_cases_vendor_payout
        FOREIGN KEY (vendor_payout_id)
        REFERENCES vendor_payouts (payout_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_cases_raised_by_one_party
        CHECK (
            (raised_by_customer_id IS NOT NULL)
            <>
            (raised_by_vendor_id IS NOT NULL)
        ),

    CONSTRAINT chk_cases_case_type
        CHECK (
            case_type IN (
                'ACCOUNT',
                'ORDER',
                'PAYMENT',
                'DELIVERY',
                'RETURN',
                'REFUND',
                'PAYOUT',
                'VENDOR',
                'OTHER'
            )
        ),

    CONSTRAINT chk_cases_priority
        CHECK (
            priority IN (
                'LOW',
                'MEDIUM',
                'HIGH',
                'CRITICAL'
            )
        ),

    CONSTRAINT chk_cases_status
        CHECK (
            status IN (
                'OPEN',
                'IN_PROGRESS',
                'WAITING_FOR_CUSTOMER',
                'WAITING_FOR_VENDOR',
                'WAITING_FOR_EXTERNAL',
                'RESOLVED',
                'CLOSED',
                'CANCELLED'
            )
        ),

    CONSTRAINT chk_cases_reason
        CHECK (BTRIM(reason) <> ''),

    CONSTRAINT chk_cases_description
        CHECK (BTRIM(description) <> ''),

    CONSTRAINT chk_cases_resolution
        CHECK (
            status NOT IN ('RESOLVED', 'CLOSED')
            OR resolution IS NOT NULL
        ),

    CONSTRAINT chk_cases_resolved_at
        CHECK (
            status NOT IN ('RESOLVED', 'CLOSED')
            OR resolved_at IS NOT NULL
        )
);

CREATE INDEX idx_cases_customer_id
    ON cases (raised_by_customer_id);

CREATE INDEX idx_cases_vendor_id
    ON cases (raised_by_vendor_id);

CREATE INDEX idx_cases_assigned_agent_id
    ON cases (assigned_agent_id);

CREATE INDEX idx_cases_status
    ON cases (status);

CREATE INDEX idx_cases_case_type
    ON cases (case_type);

CREATE INDEX idx_cases_created_at
    ON cases (created_at);

CREATE INDEX idx_cases_order_id
    ON cases (order_id);

CREATE INDEX idx_cases_order_item_id
    ON cases (order_item_id);

CREATE INDEX idx_cases_payment_id
    ON cases (payment_id);

CREATE INDEX idx_cases_delivery_id
    ON cases (delivery_id);

CREATE INDEX idx_cases_return_id
    ON cases (return_id);

CREATE INDEX idx_cases_refund_id
    ON cases (refund_id);

CREATE INDEX idx_cases_vendor_payout_id
    ON cases (vendor_payout_id);