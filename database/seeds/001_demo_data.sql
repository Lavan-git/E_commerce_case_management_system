BEGIN;

-- ============================================================
-- 1. CUSTOMERS
-- ============================================================

INSERT INTO customers (
    customer_id,
    name,
    email,
    phone,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    'Aarav Sharma',
    'aarav.sharma@example.com',
    '9876543210',
    'ACTIVE',
    NULL,
    '2026-08-01 10:00:00+05:30',
    '2026-08-01 10:00:00+05:30'
),
(
    2,
    'Priya Mehta',
    'priya.mehta@example.com',
    '9876543211',
    'ACTIVE',
    NULL,
    '2026-08-03 11:30:00+05:30',
    '2026-08-03 11:30:00+05:30'
),
(
    3,
    'Rohan Gupta',
    'rohan.gupta@example.com',
    '9876543212',
    'ACTIVE',
    NULL,
    '2026-08-05 09:15:00+05:30',
    '2026-08-05 09:15:00+05:30'
),
(
    4,
    'Sneha Iyer',
    'sneha.iyer@example.com',
    '9876543213',
    'ACTIVE',
    NULL,
    '2026-08-07 14:00:00+05:30',
    '2026-08-07 14:00:00+05:30'
);


-- ============================================================
-- 2. VENDORS
-- ============================================================

INSERT INTO vendors (
    vendor_id,
    business_name,
    legal_name,
    email,
    phone,
    gstin,
    pan,
    kyc_status,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    'TechWorld Electronics',
    'TechWorld Electronics Pvt Ltd',
    'support@techworld.example.com',
    '9810001001',
    '07AABCT1234A1Z5',
    'AABCT1234A',
    'VERIFIED',
    'ACTIVE',
    NULL,
    '2026-07-15 09:00:00+05:30',
    '2026-07-15 09:00:00+05:30'
),
(
    2,
    'HomeKart Supplies',
    'HomeKart Supplies LLP',
    'support@homekart.example.com',
    '9810001002',
    '07AABCH5678B1Z3',
    'AABCH5678B',
    'VERIFIED',
    'ACTIVE',
    NULL,
    '2026-07-18 10:30:00+05:30',
    '2026-07-18 10:30:00+05:30'
),
(
    3,
    'Urban Lifestyle Store',
    'Urban Lifestyle Store Pvt Ltd',
    'support@urbanlifestyle.example.com',
    '9810001003',
    '07AABCU9012C1Z8',
    'AABCU9012C',
    'VERIFIED',
    'ACTIVE',
    NULL,
    '2026-07-20 12:00:00+05:30',
    '2026-07-20 12:00:00+05:30'
);


-- ============================================================
-- 3. PRODUCTS
-- ============================================================

INSERT INTO products (
    product_id,
    name,
    description,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    'Wireless Headphones',
    'Over-ear wireless headphones with active noise cancellation.',
    'ACTIVE',
    NULL,
    '2026-07-21 09:00:00+05:30',
    '2026-07-21 09:00:00+05:30'
),
(
    2,
    'Mechanical Keyboard',
    'Mechanical keyboard with tactile switches.',
    'ACTIVE',
    NULL,
    '2026-07-21 09:10:00+05:30',
    '2026-07-21 09:10:00+05:30'
),
(
    3,
    'Smartphone X',
    '128 GB smartphone with OLED display.',
    'ACTIVE',
    NULL,
    '2026-07-21 09:20:00+05:30',
    '2026-07-21 09:20:00+05:30'
),
(
    4,
    'Air Fryer 5L',
    '5 litre digital air fryer.',
    'ACTIVE',
    NULL,
    '2026-07-21 09:30:00+05:30',
    '2026-07-21 09:30:00+05:30'
),
(
    5,
    'Smart Desk Lamp',
    'LED desk lamp with adjustable brightness.',
    'ACTIVE',
    NULL,
    '2026-07-21 09:40:00+05:30',
    '2026-07-21 09:40:00+05:30'
);


-- ============================================================
-- 4. VENDOR PRODUCTS
-- ============================================================

INSERT INTO vendor_products (
    vendor_product_id,
    vendor_id,
    product_id,
    price,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    899.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:00:00+05:30',
    '2026-07-22 10:00:00+05:30'
),
(
    2,
    2,
    1,
    920.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:05:00+05:30',
    '2026-07-22 10:05:00+05:30'
),
(
    3,
    1,
    2,
    1499.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:10:00+05:30',
    '2026-07-22 10:10:00+05:30'
),
(
    4,
    3,
    3,
    24999.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:15:00+05:30',
    '2026-07-22 10:15:00+05:30'
),
(
    5,
    2,
    4,
    3499.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:20:00+05:30',
    '2026-07-22 10:20:00+05:30'
),
(
    6,
    3,
    5,
    799.00,
    'ACTIVE',
    NULL,
    '2026-07-22 10:25:00+05:30',
    '2026-07-22 10:25:00+05:30'
);


-- ============================================================
-- 5. ORDERS
-- ============================================================

INSERT INTO orders (
    order_id,
    customer_id,
    ordered_at,
    total_amount,
    status,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    '2026-09-01 10:15:00+05:30',
    3897.00,
    'DELIVERED',
    '2026-09-01 10:15:00+05:30'
),
(
    2,
    1,
    '2026-09-04 14:20:00+05:30',
    3499.00,
    'SHIPPED',
    '2026-09-04 14:20:00+05:30'
),
(
    3,
    2,
    '2026-09-05 09:10:00+05:30',
    24999.00,
    'DELIVERED',
    '2026-09-05 09:10:00+05:30'
),
(
    4,
    3,
    '2026-09-06 16:45:00+05:30',
    799.00,
    'OUT_FOR_DELIVERY',
    '2026-09-06 16:45:00+05:30'
),
(
    5,
    4,
    '2026-09-07 11:30:00+05:30',
    1840.00,
    'DELIVERED',
    '2026-09-07 11:30:00+05:30'
);


-- ============================================================
-- 6. ORDER ITEMS
-- ============================================================

INSERT INTO order_items (
    order_item_id,
    order_id,
    vendor_product_id,
    quantity,
    unit_price,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    1,
    899.00,
    '2026-09-01 10:15:00+05:30'
),
(
    2,
    1,
    3,
    2,
    1499.00,
    '2026-09-01 10:15:00+05:30'
),
(
    3,
    2,
    5,
    1,
    3499.00,
    '2026-09-04 14:20:00+05:30'
),
(
    4,
    3,
    4,
    1,
    24999.00,
    '2026-09-05 09:10:00+05:30'
),
(
    5,
    4,
    6,
    1,
    799.00,
    '2026-09-06 16:45:00+05:30'
),
(
    6,
    5,
    2,
    2,
    920.00,
    '2026-09-07 11:30:00+05:30'
);


-- ============================================================
-- 7. PAYMENTS
-- ============================================================

INSERT INTO payments (
    payment_id,
    customer_id,
    order_id,
    transaction_reference,
    amount,
    payment_method,
    status,
    transaction_time,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    'PAY-1001',
    3897.00,
    'CARD',
    'SUCCESS',
    '2026-09-01 10:16:00+05:30',
    '2026-09-01 10:16:00+05:30'
),
(
    2,
    1,
    2,
    'PAY-1002',
    3499.00,
    'UPI',
    'SUCCESS',
    '2026-09-04 14:21:00+05:30',
    '2026-09-04 14:21:00+05:30'
),
(
    3,
    2,
    3,
    'PAY-1003',
    24999.00,
    'CARD',
    'SUCCESS',
    '2026-09-05 09:11:00+05:30',
    '2026-09-05 09:11:00+05:30'
),
(
    4,
    3,
    4,
    'PAY-1004',
    799.00,
    'UPI',
    'SUCCESS',
    '2026-09-06 16:46:00+05:30',
    '2026-09-06 16:46:00+05:30'
),
(
    5,
    4,
    5,
    'PAY-1005',
    1840.00,
    'CARD',
    'SUCCESS',
    '2026-09-07 11:31:00+05:30',
    '2026-09-07 11:31:00+05:30'
),
(
    6,
    2,
    NULL,
    'PAY-1006',
    1299.00,
    'UPI',
    'SUCCESS',
    '2026-09-08 13:05:00+05:30',
    '2026-09-08 13:05:00+05:30'
);


-- ============================================================
-- 8. VENDOR PAYOUTS
-- ============================================================

INSERT INTO vendor_payouts (
    payout_id,
    vendor_id,
    expected_amount,
    actual_amount,
    expected_payout_date,
    paid_at,
    status,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    5300.00,
    5300.00,
    '2026-09-10',
    '2026-09-10 12:00:00+05:30',
    'PAID',
    '2026-09-10 09:00:00+05:30'
),
(
    2,
    2,
    10000.00,
    8000.00,
    '2026-09-10',
    '2026-09-10 15:00:00+05:30',
    'PAID',
    '2026-09-10 09:05:00+05:30'
),
(
    3,
    3,
    7400.00,
    NULL,
    '2026-09-12',
    NULL,
    'PENDING',
    '2026-09-11 09:10:00+05:30'
);


-- ============================================================
-- 9. DELIVERY PERSONS
-- ============================================================

INSERT INTO delivery_persons (
    delivery_person_id,
    name,
    phone,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    'Rahul Verma',
    '9820002001',
    'ACTIVE',
    NULL,
    '2026-08-01 08:00:00+05:30',
    '2026-08-01 08:00:00+05:30'
),
(
    2,
    'Amit Singh',
    '9820002002',
    'ACTIVE',
    NULL,
    '2026-08-02 08:00:00+05:30',
    '2026-08-02 08:00:00+05:30'
),
(
    3,
    'Karan Patel',
    '9820002003',
    'ACTIVE',
    NULL,
    '2026-08-03 08:00:00+05:30',
    '2026-08-03 08:00:00+05:30'
);


-- ============================================================
-- 10. DELIVERIES
-- ============================================================

INSERT INTO deliveries (
    delivery_id,
    order_id,
    delivery_person_id,
    delivery_partner,
    tracking_number,
    status,
    shipped_at,
    expected_delivery_at,
    delivered_at,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    'FastExpress',
    'FX100001',
    'DELIVERED',
    '2026-09-02 09:00:00+05:30',
    '2026-09-03 20:00:00+05:30',
    '2026-09-03 15:25:00+05:30',
    '2026-09-01 12:00:00+05:30'
),
(
    2,
    2,
    2,
    'FastExpress',
    'FX100002',
    'IN_TRANSIT',
    '2026-09-05 10:00:00+05:30',
    '2026-09-07 20:00:00+05:30',
    NULL,
    '2026-09-04 16:00:00+05:30'
),
(
    3,
    3,
    3,
    'QuickShip',
    'QS100003',
    'DELIVERED',
    '2026-09-06 08:30:00+05:30',
    '2026-09-08 20:00:00+05:30',
    '2026-09-08 13:20:00+05:30',
    '2026-09-05 12:00:00+05:30'
),
(
    4,
    4,
    1,
    'FastExpress',
    'FX100004',
    'FAILED',
    '2026-09-07 09:00:00+05:30',
    '2026-09-09 20:00:00+05:30',
    NULL,
    '2026-09-06 18:00:00+05:30'
),
(
    5,
    5,
    2,
    'QuickShip',
    'QS100005',
    'DELIVERED',
    '2026-09-08 09:30:00+05:30',
    '2026-09-10 20:00:00+05:30',
    '2026-09-10 16:10:00+05:30',
    '2026-09-07 13:00:00+05:30'
);


-- ============================================================
-- 11. DELIVERY ATTEMPTS
-- ============================================================

INSERT INTO delivery_attempts (
    attempt_id,
    delivery_id,
    delivery_person_id,
    attempted_at,
    status,
    failure_reason,
    remarks,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    '2026-09-03 15:25:00+05:30',
    'SUCCESS',
    NULL,
    'Delivered successfully to customer.',
    '2026-09-03 15:30:00+05:30'
),
(
    2,
    2,
    2,
    '2026-09-08 18:10:00+05:30',
    'FAILED',
    'CUSTOMER_UNAVAILABLE',
    'Customer was not available at the delivery address.',
    '2026-09-08 18:15:00+05:30'
),
(
    3,
    4,
    1,
    '2026-09-08 17:20:00+05:30',
    'FAILED',
    'CUSTOMER_UNAVAILABLE',
    'Customer did not answer the delivery call.',
    '2026-09-08 17:25:00+05:30'
),
(
    4,
    4,
    1,
    '2026-09-09 18:05:00+05:30',
    'FAILED',
    'ADDRESS_ISSUE',
    'Unable to locate the delivery address.',
    '2026-09-09 18:10:00+05:30'
),
(
    5,
    5,
    2,
    '2026-09-10 16:10:00+05:30',
    'SUCCESS',
    NULL,
    'Delivered successfully.',
    '2026-09-10 16:15:00+05:30'
);


-- ============================================================
-- 12. RETURNS
-- ============================================================

INSERT INTO returns (
    return_id,
    order_item_id,
    reason,
    status,
    requested_at,
    picked_up_at,
    completed_at,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    2,
    'Keyboard has a faulty key switch.',
    'COMPLETED',
    '2026-09-05 11:00:00+05:30',
    '2026-09-06 15:00:00+05:30',
    '2026-09-08 17:00:00+05:30',
    '2026-09-05 11:00:00+05:30'
),
(
    2,
    4,
    'Phone received with a damaged screen.',
    'REQUESTED',
    '2026-09-09 10:30:00+05:30',
    NULL,
    NULL,
    '2026-09-09 10:30:00+05:30'
);


-- ============================================================
-- 13. REFUNDS
-- ============================================================

INSERT INTO refunds (
    refund_id,
    payment_id,
    return_id,
    amount,
    status,
    requested_at,
    processed_at,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    1,
    1,
    1499.00,
    'COMPLETED',
    '2026-09-05 11:30:00+05:30',
    '2026-09-09 10:00:00+05:30',
    '2026-09-05 11:30:00+05:30'
),
(
    2,
    3,
    2,
    24999.00,
    'PROCESSING',
    '2026-09-09 11:00:00+05:30',
    NULL,
    '2026-09-09 11:00:00+05:30'
);


-- ============================================================
-- 14. SUPPORT AGENTS
-- ============================================================

INSERT INTO support_agents (
    agent_id,
    name,
    email,
    status,
    deleted_at,
    created_at,
    updated_at
)
OVERRIDING SYSTEM VALUE
VALUES
(
    1,
    'Neha Kapoor',
    'neha.kapoor@support.example.com',
    'ACTIVE',
    NULL,
    '2026-08-01 09:00:00+05:30',
    '2026-08-01 09:00:00+05:30'
),
(
    2,
    'Vikram Joshi',
    'vikram.joshi@support.example.com',
    'ACTIVE',
    NULL,
    '2026-08-02 09:00:00+05:30',
    '2026-08-02 09:00:00+05:30'
),
(
    3,
    'Ananya Rao',
    'ananya.rao@support.example.com',
    'ACTIVE',
    NULL,
    '2026-08-03 09:00:00+05:30',
    '2026-08-03 09:00:00+05:30'
);


-- ============================================================
-- 15. CASES
-- ============================================================

INSERT INTO cases (
    case_id,
    raised_by_customer_id,
    raised_by_vendor_id,
    case_type,
    category,
    reason,
    description,
    priority,
    status,
    assigned_agent_id,
    order_id,
    order_item_id,
    payment_id,
    delivery_id,
    return_id,
    refund_id,
    vendor_payout_id,
    resolution,
    created_at,
    updated_at,
    resolved_at
)
OVERRIDING SYSTEM VALUE
VALUES

-- 1. Customer account case
(
    1,
    1,
    NULL,
    'ACCOUNT',
    'PROFILE',
    'Update mobile number',
    'Customer wants to update the mobile number associated with the account.',
    'LOW',
    'IN_PROGRESS',
    1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    '2026-09-09 09:00:00+05:30',
    '2026-09-09 10:00:00+05:30',
    NULL
),

-- 2. Wrong product/item case
(
    2,
    1,
    NULL,
    'ORDER',
    'WRONG_ITEM',
    'Wrong item received',
    'Customer reports that the item received does not match the ordered product.',
    'HIGH',
    'RESOLVED',
    2,
    1,
    1,
    NULL,
    1,
    NULL,
    NULL,
    NULL,
    'Customer was provided a replacement and the incorrect item was scheduled for return.',
    '2026-09-04 18:00:00+05:30',
    '2026-09-06 16:00:00+05:30',
    '2026-09-06 16:00:00+05:30'
),

-- 3. Payment succeeded but order wasn't created
(
    3,
    2,
    NULL,
    'PAYMENT',
    'PAYMENT_WITHOUT_ORDER',
    'Payment deducted but order not created',
    'Customer was charged successfully but no corresponding order was created.',
    'CRITICAL',
    'OPEN',
    1,
    NULL,
    NULL,
    6,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    '2026-09-08 13:20:00+05:30',
    '2026-09-08 14:00:00+05:30',
    NULL
),

-- 4. Order not delivered
(
    4,
    3,
    NULL,
    'DELIVERY',
    'NOT_DELIVERED',
    'Order not delivered after multiple attempts',
    'Customer reports that the order has not been delivered despite two failed delivery attempts.',
    'HIGH',
    'IN_PROGRESS',
    2,
    4,
    5,
    NULL,
    4,
    NULL,
    NULL,
    NULL,
    NULL,
    '2026-09-10 09:00:00+05:30',
    '2026-09-10 10:00:00+05:30',
    NULL
),

-- 5. Return case
(
    5,
    2,
    NULL,
    'RETURN',
    'RETURN_PENDING',
    'Return request not processed',
    'Customer requested a return for a damaged smartphone but pickup has not yet been arranged.',
    'HIGH',
    'WAITING_FOR_EXTERNAL',
    3,
    3,
    4,
    3,
    3,
    2,
    NULL,
    NULL,
    NULL,
    '2026-09-09 11:30:00+05:30',
    '2026-09-10 09:00:00+05:30',
    NULL
),

-- 6. Refund case
(
    6,
    2,
    NULL,
    'REFUND',
    'REFUND_PENDING',
    'Refund has not been completed',
    'Customer is waiting for the refund following an approved return.',
    'HIGH',
    'IN_PROGRESS',
    3,
    3,
    4,
    3,
    NULL,
    2,
    2,
    NULL,
    NULL,
    '2026-09-10 11:00:00+05:30',
    '2026-09-10 12:00:00+05:30',
    NULL
),

-- 7. Vendor payout discrepancy
(
    7,
    NULL,
    2,
    'PAYOUT',
    'PAYOUT_DISCREPANCY',
    'Payout amount is lower than expected',
    'Vendor expected a payout of INR 10000 but received only INR 8000.',
    'HIGH',
    'RESOLVED',
    2,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    2,
    'Payout discrepancy was verified and an additional INR 2000 adjustment was initiated.',
    '2026-09-10 16:00:00+05:30',
    '2026-09-11 15:00:00+05:30',
    '2026-09-11 15:00:00+05:30'
),

-- 8. Vendor payout delayed
(
    8,
    NULL,
    3,
    'PAYOUT',
    'PAYOUT_DELAY',
    'Expected payout has not been received',
    'Vendor has not received the payout scheduled for 12 September.',
    'MEDIUM',
    'OPEN',
    1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    3,
    NULL,
    '2026-09-12 10:00:00+05:30',
    '2026-09-12 10:00:00+05:30',
    NULL
),

-- 9. Vendor dashboard issue
(
    9,
    NULL,
    1,
    'VENDOR',
    'DASHBOARD',
    'Unable to view sales dashboard',
    'Vendor reports that the sales dashboard is not displaying current order information.',
    'MEDIUM',
    'IN_PROGRESS',
    3,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    '2026-09-11 14:00:00+05:30',
    '2026-09-11 14:30:00+05:30',
    NULL
);


-- ============================================================
-- 16. CASE UPDATES
-- ============================================================

INSERT INTO case_updates (
    update_id,
    case_id,
    updated_by_agent_id,
    source,
    old_status,
    new_status,
    comment,
    created_at
)
OVERRIDING SYSTEM VALUE
VALUES

(
    1,
    1,
    1,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Customer identity verified. Profile update request is being processed.',
    '2026-09-09 10:00:00+05:30'
),

(
    2,
    2,
    2,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Verified the order item and delivery information.',
    '2026-09-04 20:00:00+05:30'
),

(
    3,
    2,
    2,
    'AGENT',
    'IN_PROGRESS',
    'RESOLVED',
    'Replacement approved and return process initiated for incorrect item.',
    '2026-09-06 16:00:00+05:30'
),

(
    4,
    3,
    1,
    'AGENT',
    'OPEN',
    'OPEN',
    'Payment transaction confirmed. Order creation failure requires further investigation.',
    '2026-09-08 14:00:00+05:30'
),

(
    5,
    4,
    2,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Two failed delivery attempts confirmed. Escalated to delivery operations.',
    '2026-09-10 10:00:00+05:30'
),

(
    6,
    5,
    3,
    'AGENT',
    'OPEN',
    'WAITING_FOR_EXTERNAL',
    'Return request verified. Waiting for pickup scheduling.',
    '2026-09-10 09:00:00+05:30'
),

(
    7,
    6,
    3,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Refund request confirmed and is currently being processed.',
    '2026-09-10 12:00:00+05:30'
),

(
    8,
    7,
    2,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Compared expected and actual payout amounts and confirmed discrepancy.',
    '2026-09-10 17:00:00+05:30'
),

(
    9,
    7,
    2,
    'AGENT',
    'IN_PROGRESS',
    'RESOLVED',
    'Additional payout adjustment initiated for the missing amount.',
    '2026-09-11 15:00:00+05:30'
),

(
    10,
    8,
    1,
    'SYSTEM',
    NULL,
    'OPEN',
    'Automated payout monitoring detected a pending vendor payout.',
    '2026-09-12 10:00:00+05:30'
),

(
    11,
    9,
    3,
    'AGENT',
    'OPEN',
    'IN_PROGRESS',
    'Dashboard issue reproduced and forwarded for technical investigation.',
    '2026-09-11 14:30:00+05:30'
);


-- ============================================================
-- RESET IDENTITY SEQUENCES
-- This allows future normal INSERTs to continue after the
-- explicitly seeded IDs.
-- ============================================================

SELECT setval(
    pg_get_serial_sequence('customers', 'customer_id'),
    COALESCE((SELECT MAX(customer_id) FROM customers), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('vendors', 'vendor_id'),
    COALESCE((SELECT MAX(vendor_id) FROM vendors), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('products', 'product_id'),
    COALESCE((SELECT MAX(product_id) FROM products), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('vendor_products', 'vendor_product_id'),
    COALESCE((SELECT MAX(vendor_product_id) FROM vendor_products), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('orders', 'order_id'),
    COALESCE((SELECT MAX(order_id) FROM orders), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('order_items', 'order_item_id'),
    COALESCE((SELECT MAX(order_item_id) FROM order_items), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('payments', 'payment_id'),
    COALESCE((SELECT MAX(payment_id) FROM payments), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('vendor_payouts', 'payout_id'),
    COALESCE((SELECT MAX(payout_id) FROM vendor_payouts), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('delivery_persons', 'delivery_person_id'),
    COALESCE((SELECT MAX(delivery_person_id) FROM delivery_persons), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('deliveries', 'delivery_id'),
    COALESCE((SELECT MAX(delivery_id) FROM deliveries), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('delivery_attempts', 'attempt_id'),
    COALESCE((SELECT MAX(attempt_id) FROM delivery_attempts), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('returns', 'return_id'),
    COALESCE((SELECT MAX(return_id) FROM returns), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('refunds', 'refund_id'),
    COALESCE((SELECT MAX(refund_id) FROM refunds), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('support_agents', 'agent_id'),
    COALESCE((SELECT MAX(agent_id) FROM support_agents), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('cases', 'case_id'),
    COALESCE((SELECT MAX(case_id) FROM cases), 1),
    true
);

SELECT setval(
    pg_get_serial_sequence('case_updates', 'update_id'),
    COALESCE((SELECT MAX(update_id) FROM case_updates), 1),
    true
);

COMMIT;