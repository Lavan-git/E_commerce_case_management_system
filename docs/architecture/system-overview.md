# System Overview

## 1. Purpose

The E-commerce Dispute Resolution & Case Management System is a backend application responsible for managing disputes raised by customers and vendors.

The application does not attempt to recreate a complete e-commerce marketplace.

Instead, it provides a dedicated case-management layer that connects disputes to existing e-commerce business records.

The system is designed so that a support agent can start with a case and trace the relevant business information through related entities.

For example:

```text
Case
  |
  +-- Customer
  |
  +-- Order
       |
       +-- Order Item
       |
       +-- Delivery
       |     |
       |     +-- Delivery Attempts
       |
       +-- Payment
       |
       +-- Return
             |
             +-- Refund
```

## 2. High-Level Architecture

```text
                    +-------------------+
                    |      Client       |
                    | Browser / API     |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   FastAPI API     |
                    |     Layer         |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   Service Layer   |
                    | Business Rules    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Repository Layer  |
                    | Data Access       |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | SQLAlchemy ORM    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |    PostgreSQL     |
                    +-------------------+
```

Cross-cutting concerns:

```text
Request Validation
       |
Exception Handling
       |
Structured Logging
       |
Request ID Middleware
```

## 3. Application Layers

### API Layer

The API layer is responsible for:

- Receiving HTTP requests
- Validating request data
- Calling application services
- Returning response models
- Mapping application errors to HTTP responses

FastAPI is used for API routing and request/response validation.

The API layer should not contain database queries or significant business rules.

### Service Layer

The service layer contains business logic.

Examples include:

- Validating supported case types
- Validating priorities
- Validating case status transitions
- Enforcing resolution requirements
- Creating the initial case history record
- Managing transaction-level operations

The service layer is intentionally independent of HTTP-specific behavior.

### Repository Layer

Repositories encapsulate database access.

The case repository currently supports:

- Creating a case
- Retrieving a case
- Listing cases
- Updating a case

Repositories do not own the application-level business rules.

Transaction decisions are handled by the service layer.

### ORM Layer

SQLAlchemy provides Python representations of the PostgreSQL schema.

The ORM models use SQLAlchemy 2.x typed mappings.

Relationships are explicitly represented using foreign keys and `relationship()` definitions.

The ORM reflects the database schema rather than being used to automatically generate the schema.

## 4. Central Domain Entity

The `cases` table is the central domain entity.

Each case must have exactly one actor:

```text
Customer OR Vendor
```

This rule is enforced at the database level.

A case may additionally reference one or more related business records.

Examples:

```text
Payment Case
    -> Payment

Delivery Case
    -> Order
    -> Delivery
    -> Delivery Attempts

Refund Case
    -> Return
    -> Refund
    -> Payment

Payout Case
    -> Vendor Payout
    -> Vendor
```

## 5. Case Lifecycle

A typical case lifecycle is:

```text
OPEN
  |
  v
IN_PROGRESS
  |
  +--------------------+
  |                    |
  v                    v
WAITING_FOR_CUSTOMER   WAITING_FOR_VENDOR
  |                    |
  +---------+----------+
            |
            v
        IN_PROGRESS
            |
            v
        RESOLVED
            |
            v
          CLOSED
```

Cases may also be cancelled when appropriate.

The service layer validates status transitions rather than allowing arbitrary status changes.

## 6. Case History

`case_updates` provides an append-oriented history of changes made to cases.

Each update can identify:

- The case
- The actor performing the update
- The source of the update
- The previous status
- The new status
- A comment
- Timestamp

The supported sources are:

```text
AGENT
SYSTEM
AI
```

`AI` is included to support future intelligent case-management workflows without changing the database model.

## 7. Transaction Boundaries

The service layer owns transaction decisions.

For example, creating a case performs:

```text
1. Create Case
2. Create initial Case Update
3. Commit transaction
```

Both operations belong to the same transaction.

If an error occurs, the transaction is rolled back.

Repositories therefore do not independently commit every operation.

## 8. Database Design Principles

The database follows several principles.

### Normalize facts

Each business fact is stored in its appropriate entity.

For example:

- Current vendor listing price belongs to `vendor_products`
- Actual purchased price belongs to `order_items`
- Payment transaction information belongs to `payments`
- Case history belongs to `case_updates`

### Avoid unnecessary duplication

The system does not store fields such as:

```text
vendor_name
product_name
customer_name
current_product_price
```

inside the case table.

Those values are obtained through relationships.

### Preserve historical values

Values that may change over time but are important to historical records are copied intentionally.

For example:

```text
vendor_products.price
```

represents the current listing price, while:

```text
order_items.unit_price
```

represents the price actually used for that purchase.

## 9. Deletion Strategy

Foreign keys generally use:

```text
ON DELETE RESTRICT
```

This prevents accidental deletion of records that are required for historical traceability.

Soft deletion is used selectively for master-like entities such as:

- Customers
- Vendors
- Products
- Delivery persons
- Support agents

Transactional records such as cases, payments, orders, returns, and refunds are not automatically soft-deleted.

## 10. Logging and Observability

Every HTTP request receives a request ID.

The middleware records:

- Request ID
- HTTP status code
- Request duration
- Request lifecycle events

Logs are emitted as JSON so that they can later be consumed by centralized logging and observability systems.

This design prepares the application for future monitoring and production deployment.
