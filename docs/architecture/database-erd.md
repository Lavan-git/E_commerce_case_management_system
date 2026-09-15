# Database ERD

## 1. Overview

The database consists of 16 tables.

The design separates:

- Marketplace/master data
- Transactional data
- Delivery information
- Financial information
- Case-management information

The central application entity is `cases`.

## 2. Entity Relationship Overview

```text
customers
    |
    +--------------------< orders
    |                       |
    |                       +----< order_items >---- vendor_products >---- vendors
    |                                           |
    |                                           +---- products
    |
    +--------------------< payments
    |
    +--------------------< cases
                              |
                              +---- case_updates
                              |
                              +---- support_agents

orders
    |
    +----< deliveries
    |        |
    |        +----< delivery_attempts
    |                   |
    |                   +---- delivery_persons
    |
    +----< order_items
    |
    +----< payments

order_items
    |
    +----< returns
               |
               +----< refunds
                         |
                         +---- payments

vendors
    |
    +----< vendor_products
    |
    +----< vendor_payouts
                |
                +---- cases
```

## 3. Core Tables

### customers

Stores customer master information.

Important fields:

- `customer_id`
- `name`
- `email`
- `phone`
- `status`
- `deleted_at`

### vendors

Stores vendor master information.

Important fields:

- `vendor_id`
- `business_name`
- `legal_name`
- `email`
- `phone`
- `gstin`
- `pan`
- `kyc_status`
- `status`
- `deleted_at`

### products

Stores product-level information independent of any specific vendor.

Important fields:

- `product_id`
- `name`
- `description`
- `status`

### vendor_products

Represents a vendor's listing of a product.

Important fields:

- `vendor_product_id`
- `vendor_id`
- `product_id`
- `price`
- `status`

This table allows the same product to be sold by multiple vendors.

## 4. Order Tables

### orders

Represents a customer order.

Important fields:

- `order_id`
- `customer_id`
- `order_number`
- `ordered_at`
- `total_amount`
- `status`

An order is not directly associated with a vendor because one order may contain products from multiple vendors.

### order_items

Represents individual products purchased within an order.

Important fields:

- `order_item_id`
- `order_id`
- `vendor_product_id`
- `quantity`
- `unit_price`

`unit_price` stores the actual purchase price at the time of the order.

Therefore, later changes to the vendor's listing price do not alter historical order data.

## 5. Payment Tables

### payments

Stores payment transactions.

Important fields:

- `payment_id`
- `customer_id`
- `order_id`
- `transaction_reference`
- `amount`
- `method`
- `status`
- `transaction_time`

`order_id` is nullable because a payment can exist without a successfully created order.

This supports disputes such as:

```text
Payment successful
        |
        v
Order does not exist
        |
        v
Payment-related case
```

### vendor_payouts

Stores payout information for vendors.

Important fields:

- `vendor_payout_id`
- `vendor_id`
- `expected_amount`
- `actual_amount`
- `expected_payout_date`
- `paid_at`
- `status`

This allows payout discrepancies to be represented without storing duplicate vendor information.

## 6. Delivery Tables

### delivery_persons

Stores delivery-person information.

### deliveries

Represents delivery information for an order.

Important relationships:

```text
orders
  |
  +---- deliveries
           |
           +---- delivery_persons
```

### delivery_attempts

Stores each delivery attempt.

This table exists because a delivery can have multiple attempts.

For example:

```text
Delivery #4

Attempt 1 -> FAILED -> CUSTOMER_UNAVAILABLE
Attempt 2 -> FAILED -> ADDRESS_ISSUE
```

The delivery person can also change between attempts.

## 7. Return and Refund Tables

### returns

Represents a return request for an individual order item.

Important fields:

- `return_id`
- `order_item_id`
- `reason`
- `status`
- `requested_at`
- `picked_up_at`
- `completed_at`

### refunds

Represents money returned to a customer.

Important relationships:

```text
order_item
    |
    +---- return
            |
            +---- refund
                    |
                    +---- payment
```

`return_id` is nullable because a refund does not always have to be associated with a return workflow.

## 8. Case Management Tables

### support_agents

Stores support-agent information.

Important fields:

- `support_agent_id`
- `name`
- `email`
- `status`

### cases

This is the central application table.

A case can be raised by:

```text
customer
OR
vendor
```

The database enforces this requirement.

Cases can be associated with:

- Orders
- Order items
- Payments
- Deliveries
- Returns
- Refunds
- Vendor payouts
- Support agents

### case_updates

Stores the history of case changes.

Important fields:

- `case_update_id`
- `case_id`
- `updated_by_agent_id`
- `source`
- `old_status`
- `new_status`
- `comment`
- `created_at`

## 9. Foreign Key Strategy

Foreign keys generally use:

```sql
ON DELETE RESTRICT
```

The purpose is to protect historical records.

For example, deleting a customer should not silently destroy:

- Orders
- Payments
- Cases
- Returns
- Refunds

The database therefore prevents destructive deletion when dependent records exist.

## 10. Important Constraints

Several business rules are enforced directly by the database.

### Case actor constraint

A case must belong to exactly one actor:

```text
customer XOR vendor
```

### Case resolution constraint

Cases marked:

```text
RESOLVED
CLOSED
```

must have resolution information and a resolution timestamp.

### Delivery attempt constraint

A failed delivery attempt must contain a failure reason.

### Positive monetary values

Amounts such as:

- payment amount
- refund amount
- payout amount
- product price

must be greater than zero where applicable.

## 11. Why the Model Uses 16 Tables

The design intentionally avoids both extremes:

```text
One giant table
        VS
Dozens of unnecessary micro-tables
```

The 16-table model separates meaningful business concepts while avoiding redundant copies of the same information.

The database is designed to be sufficient for case management while remaining extensible for later training phases.
