# API Design

## 1. Overview

The application exposes a REST API for case-management operations.

The API is implemented using FastAPI.

Base path:

```text
/api/v1
```

The API intentionally focuses on case-related operations.

It does not provide general CRUD APIs for:

- Customers
- Vendors
- Products
- Orders
- Payments
- Deliveries

Those entities exist primarily to provide context and traceability for disputes.

## 2. Endpoints

### Health Check

```http
GET /api/v1/health
```

Returns the current application health status.

Example response:

```json
{
  "status": "ok"
}
```

### Create Case

```http
POST /api/v1/cases
```

Creates a new case and its initial case-history entry.

Example request:

```json
{
  "raised_by_customer_id": 4,
  "case_type": "PAYMENT",
  "category": "DUPLICATE_PAYMENT",
  "description": "Customer believes the payment was charged twice.",
  "priority": "HIGH",
  "payment_id": 1
}
```

A case must be raised by exactly one actor:

```text
raised_by_customer_id
OR
raised_by_vendor_id
```

but not both.

Example response:

```json
{
  "case_id": 10,
  "raised_by_customer_id": 4,
  "raised_by_vendor_id": null,
  "case_type": "PAYMENT",
  "category": "DUPLICATE_PAYMENT",
  "description": "Customer believes the payment was charged twice.",
  "priority": "HIGH",
  "status": "OPEN",
  "assigned_agent_id": null,
  "order_id": null,
  "order_item_id": null,
  "payment_id": 1,
  "delivery_id": null,
  "return_id": null,
  "refund_id": null,
  "vendor_payout_id": null,
  "resolution": null,
  "created_at": "...",
  "updated_at": "...",
  "resolved_at": null
}
```

## 3. List Cases

```http
GET /api/v1/cases
```

Returns cases ordered by most recently created first.

### Supported filters

```text
status
case_type
priority
assigned_agent_id
```

Example:

```http
GET /api/v1/cases?status=OPEN&priority=HIGH
```

The filters are optional and can be combined.

## 4. Get Case

```http
GET /api/v1/cases/{case_id}
```

Returns a single case.

Example:

```http
GET /api/v1/cases/4
```

If the case does not exist:

```http
404 Not Found
```

Example error:

```json
{
  "error": {
    "code": "CASE_NOT_FOUND",
    "message": "Case with id 999 was not found.",
    "request_id": "..."
  }
}
```

## 5. Update Case

```http
PATCH /api/v1/cases/{case_id}
```

Updates supported case fields.

Example request:

```json
{
  "status": "RESOLVED",
  "priority": "HIGH",
  "resolution": "Refund approved and initiated."
}
```

The service layer validates:

- Status values
- Status transitions
- Priority values
- Resolution requirements

When the status changes, a new `case_updates` record is created.

## 6. Request Validation

Pydantic models are used to validate API input.

Unexpected fields are rejected.

For example, sending:

```json
{
  "priority": "HIGH",
  "unknown_field": "value"
}
```

results in a validation error.

The API returns:

```http
422 Unprocessable Entity
```

with a consistent response structure.

Example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {
        "type": "extra_forbidden",
        "loc": [
          "body",
          "unknown_field"
        ],
        "msg": "Extra inputs are not permitted."
      }
    ],
    "request_id": "..."
  }
}
```

## 7. Error Contract

Application errors use the following structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable explanation.",
    "request_id": "request-id"
  }
}
```

Validation errors may additionally contain:

```json
"details": []
```

This provides a predictable error contract for clients.

## 8. HTTP Status Codes

The API uses standard HTTP response codes.

| Status | Meaning |
|---|---|
| 200 | Successful retrieval/update |
| 201 | Successful resource creation |
| 404 | Resource not found |
| 400 | Invalid business operation |
| 422 | Request validation failure |
| 500 | Unexpected server error |

## 9. Request IDs

Each request receives a request ID.

The client may provide:

```http
X-Request-ID: abc-123
```

If the client does not provide one, the application generates a UUID.

The request ID is returned in:

```http
X-Request-ID
```

and included in structured logs.

This provides request-level traceability.

## 10. OpenAPI Documentation

FastAPI automatically generates OpenAPI documentation.

When the development server is running:

```text
/docs
```

provides the Swagger UI interface.

The OpenAPI schema is also available through:

```text
/openapi.json
```

## 11. API Design Principles

### Thin API Layer

Route handlers should primarily:

1. Receive input
2. Call the service layer
3. Return a response

Business rules should not be implemented directly inside route handlers.

### Business Logic in Services

Case validation and status transition rules belong in the service layer.

### Database Access in Repositories

Database queries belong in repositories.

### Consistent Errors

Clients should receive predictable error structures regardless of which application layer raises the error.

### Versioned API

The API is versioned under:

```text
/api/v1
```

This allows future API changes without breaking existing clients.
