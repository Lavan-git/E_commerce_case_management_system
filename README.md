# E-commerce Dispute Resolution & Case Management System

A backend case-management system for handling customer and vendor disputes arising from an e-commerce platform.

The system focuses on the dispute-resolution workflow rather than implementing a complete e-commerce platform. Existing e-commerce entities such as customers, vendors, orders, payments, deliveries, returns, refunds, and vendor payouts are represented only to the extent required for case management and traceability.

## Project Objective

The system provides a structured way to:

- Create and manage customer and vendor dispute cases
- Associate a case with relevant e-commerce records
- Assign cases to support agents
- Track case status and priority
- Maintain a history of case updates
- Support future AI-assisted case handling
- Provide a REST API for case-management operations
- Persist all data in PostgreSQL

## Architecture

```text
Client
   |
   v
FastAPI API Layer
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
SQLAlchemy ORM
   |
   v
PostgreSQL
```

Supporting components include:

- Request validation
- Centralized exception handling
- Structured JSON logging
- Request ID middleware
- Automated tests
- OpenAPI documentation

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Database Driver | psycopg |
| Validation | Pydantic |
| Testing | pytest |
| Coverage | coverage.py |
| API Documentation | OpenAPI / Swagger UI |
| Version Control | Git |

## Repository Structure

```text
.
├── database/
│   ├── schema/
│   │   ├── 001_customers.sql
│   │   ├── 002_vendors.sql
│   │   ├── 003_products.sql
│   │   ├── 004_vendor_products.sql
│   │   ├── 005_orders.sql
│   │   ├── 006_order_items.sql
│   │   ├── 007_payments.sql
│   │   ├── 008_vendor_payouts.sql
│   │   ├── 009_delivery_persons.sql
│   │   ├── 010_deliveries.sql
│   │   ├── 011_delivery_attempts.sql
│   │   ├── 012_returns.sql
│   │   ├── 013_refunds.sql
│   │   ├── 014_support_agents.sql
│   │   ├── 015_cases.sql
│   │   ├── 016_case_updates.sql
│   │   └── 017_triggers.sql
│   ├── seeds/
│   │   └── 001_demo_data.sql
│   └── README.md
│
├── docs/
│   ├── architecture/
│   │   ├── system-overview.md
│   │   └── database-erd.md
│   ├── api/
│   │   └── api-design.md
│   └── development/
│       └── setup.md
│
├── src/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── exceptions/
│       ├── repositories/
│       ├── schemas/
│       └── services/
│
├── tests/
│   ├── api/
│   ├── integration/
│   └── unit/
│
├── .env.example
├── README.md
└── ...
```

## Database

The application uses PostgreSQL as its primary database.

The schema contains 16 application tables:

1. Customers
2. Vendors
3. Products
4. Vendor Products
5. Orders
6. Order Items
7. Payments
8. Vendor Payouts
9. Delivery Persons
10. Deliveries
11. Delivery Attempts
12. Returns
13. Refunds
14. Support Agents
15. Cases
16. Case Updates

The database schema is maintained using SQL migration-style files under `database/schema/`.

The application does not automatically create or modify database tables through `Base.metadata.create_all()`.

The SQL schema is the authoritative source for database structure.

## Case Management

The `cases` table is the central application entity.

A case may be raised by either:

- A customer
- A vendor

A case can reference related business records such as:

- Orders
- Order items
- Payments
- Deliveries
- Returns
- Refunds
- Vendor payouts

Cases support multiple statuses and priorities.

### Case Statuses

```text
OPEN
IN_PROGRESS
WAITING_FOR_CUSTOMER
WAITING_FOR_VENDOR
WAITING_FOR_EXTERNAL
RESOLVED
CLOSED
CANCELLED
```

### Case Priorities

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Case Types

```text
ACCOUNT
ORDER
PAYMENT
DELIVERY
RETURN
REFUND
PAYOUT
VENDOR
OTHER
```

Every case also maintains a history of updates through `case_updates`.

## API

The current REST API exposes case-management operations.

### Health Check

```http
GET /api/v1/health
```

### Create Case

```http
POST /api/v1/cases
```

### List Cases

```http
GET /api/v1/cases
```

Supported filters include:

- `status`
- `case_type`
- `priority`
- `assigned_agent_id`

### Get Case

```http
GET /api/v1/cases/{case_id}
```

### Update Case

```http
PATCH /api/v1/cases/{case_id}
```

Interactive API documentation is available through FastAPI's generated OpenAPI interfaces.

## Error Handling

The API uses a consistent error response structure.

Example:

```json
{
  "error": {
    "code": "CASE_NOT_FOUND",
    "message": "Case with id 999 was not found.",
    "request_id": "8ef1b3b5-1e2c-44a9-bc2c-15a7f8d91d4a"
  }
}
```

Validation failures use a dedicated error code and include safe validation details.

## Logging

The application uses structured JSON logging.

Each request receives a request ID.

The request ID is:

- Generated automatically when not provided
- Accepted from an incoming `X-Request-ID` header
- Returned in the response using the same header

This allows requests to be traced across logs.

Example:

```json
{
  "timestamp": "2026-09-15T10:30:00+00:00",
  "level": "INFO",
  "logger": "app.http",
  "message": "http.request",
  "request_id": "8ef1b3b5-1e2c-44a9-bc2c-15a7f8d91d4a",
  "status_code": 200,
  "duration_ms": 12.41
}
```

## Testing

Tests are divided into:

```text
tests/
├── api/
├── integration/
└── unit/
```

The test suite covers:

- Health endpoint
- Case creation
- Case retrieval
- Case listing
- Case filtering
- Case updates
- Validation failures
- Repository operations
- Service-layer behavior
- Database relationships

Run the test suite with:

```bash
pytest -q
```

Run coverage with:

```bash
coverage run -m pytest
coverage report
```

## Development Status

The project currently includes:

- PostgreSQL database schema
- Seed data
- SQLAlchemy ORM models
- Repository layer
- Service layer
- FastAPI endpoints
- Request validation
- Exception handling
- Structured logging
- Request tracing
- Unit, integration, and API tests
- API documentation through OpenAPI

The later training phases will extend the system toward data pipelines, RAG, tool-enabled AI workflows, human approval, authentication, observability, CI/CD, and deployment.

## License

This project is developed as part of the KPMG Fresher AI Engineering training program.
