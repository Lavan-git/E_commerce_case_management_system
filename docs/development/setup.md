# Development Setup

## 1. Prerequisites

The following tools are required:

- Python 3.12+
- PostgreSQL
- Git
- pip
- Virtual environment support

Verify Python:

```bash
python --version
```

Verify PostgreSQL:

```bash
psql --version
```

Verify Git:

```bash
git --version
```

## 2. Clone the Repository

```bash
git clone <repository-url>
cd Case_management
```

## 3. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies

Install the project dependencies:

```bash
pip install -r requirements.txt
```

If development dependencies are separated, install them as appropriate for the repository configuration.

## 5. Configure PostgreSQL

Create the application database:

```sql
CREATE DATABASE ecommerce_dispute_resolution;
```

The application expects PostgreSQL to be available locally.

Default connection details:

```text
Host: localhost
Port: 5432
Database: ecommerce_dispute_resolution
User: postgres
```

## 6. Configure Environment Variables

Create a `.env` file in the repository root.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_dispute_resolution
APP_NAME=E-commerce Dispute Resolution
DEBUG=true
```

Do not commit `.env`.

Use `.env.example` as the template for environment configuration.

## 7. Apply Database Schema

The SQL schema is maintained under:

```text
database/schema/
```

The files should be executed in numerical order.

Example using PostgreSQL:

```bash
psql -U postgres -d ecommerce_dispute_resolution -f database/schema/001_customers.sql
```

Continue through:

```text
017_triggers.sql
```

The application does not use:

```python
Base.metadata.create_all()
```

to create the production/application schema.

The SQL files are the authoritative schema definition.

## 8. Load Demo Data

After applying the schema:

```bash
psql -U postgres -d ecommerce_dispute_resolution -f database/seeds/001_demo_data.sql
```

The seed data provides realistic records for:

- Customers
- Vendors
- Products
- Vendor listings
- Orders
- Order items
- Payments
- Payouts
- Deliveries
- Delivery attempts
- Returns
- Refunds
- Support agents
- Cases
- Case updates

## 9. Run the Application

From the repository root:

```bash
uvicorn src.app.main:app --reload
```

The application should be available at:

```text
http://127.0.0.1:8000
```

## 10. API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

Health check:

```text
http://127.0.0.1:8000/api/v1/health
```

## 11. Run Tests

Run the complete test suite:

```bash
pytest -q
```

Run a specific test group:

```bash
pytest tests/unit -q
pytest tests/integration -q
pytest tests/api -q
```

## 12. Run Coverage

Run tests with coverage:

```bash
coverage run -m pytest
```

Generate the report:

```bash
coverage report
```

Optional HTML report:

```bash
coverage html
```

The generated report will be available under:

```text
htmlcov/
```

## 13. Development Workflow

A typical development workflow is:

```text
Create feature branch
        |
        v
Implement change
        |
        v
Run tests
        |
        v
Run coverage
        |
        v
Review git diff
        |
        v
Commit change
        |
        v
Push branch
        |
        v
Open Pull Request
```

Example:

```bash
git checkout develop
git checkout -b feature/<feature-name>
```

After making changes:

```bash
pytest -q
git diff --check
git status
```

Then commit:

```bash
git add .
git commit -m "feat: <description>"
```

## 14. Project Conventions

### Database

Do not modify database structure only through ORM models.

Update the SQL schema first, then keep the SQLAlchemy models synchronized with it.

### Transactions

Repositories should not independently commit every database operation.

Transaction boundaries are controlled by the service/application layer.

### API

Business logic should remain outside route handlers.

### Error Handling

Use the application's exception classes rather than returning inconsistent custom error structures from individual endpoints.

### Logging

Use the configured application logging system rather than printing directly with `print()`.

### Tests

New functionality should include appropriate unit, integration, or API tests.

## 15. Troubleshooting

### Database Connection Error

Verify:

```text
PostgreSQL is running
DATABASE_URL is correct
Database exists
Username/password are correct
```

### Import Errors

Ensure the virtual environment is active:

```bash
.venv\Scripts\activate
```

and dependencies are installed.

### Test Database Issues

Tests currently use the configured application database and seeded data.

Avoid tests that depend on fixed total record counts when the database may contain additional valid records created during API testing.

Prefer assertions such as:

```python
assert results
assert all(case.case_type == "DELIVERY" for case in results)
```

rather than:

```python
assert len(results) == 3
```
