# E-commerce Dispute Resolution & Case Management System

A backend case-management system for handling customer-side and vendor-side disputes in an e-commerce environment.

The system does **not** recreate an e-commerce platform such as Amazon or Flipkart. Instead, it focuses on the data, APIs, processing pipelines, and AI capabilities required to manage disputes and resolutions on top of an existing commerce platform.

## Project Goals

The system is designed to support cases such as:

- Customer received the wrong order.
- Order was not delivered.
- Payment was deducted but an order was not created.
- Refund or return was not initiated correctly.
- Customer account/profile issues.
- Vendor payout was delayed or incorrect.
- Vendor dashboard or operational issues.

The project is being developed as a progressive enterprise AI engineering system:

```text
Week 1  -> Case-management backend
Week 2  -> Enterprise data pipeline + Docker
Week 3  -> RAG
Week 4  -> Tools, workflows, human approval, RBAC, guardrails, observability
Week 5  -> Integration, hardening, CI/CD and final demo
```

## Architecture

At a high level, the system currently contains two major paths.

### Case-management application

```text
Client
  |
  v
FastAPI API
  |
  v
Service layer
  |
  v
Repository layer
  |
  v
PostgreSQL
```

### Enterprise data pipeline

```text
CSV / JSON / Parquet sources
            |
            v
       Source adapters
            |
            v
         Raw layer
            |
            v
      Standardization
            |
            v
     Contract validation
            |
            v
       Quality checks
        /          \
       /            \
      v              v
Valid records    Rejected records
      |              |
      v              v
Incremental      Quarantine
filtering
      |
      v
Curated layer
      |
      v
PostgreSQL
      |
      v
Pipeline audit
```

The pipeline is designed to be **incremental, idempotent, auditable, and source-agnostic**.

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic / pydantic-settings
- SQLAlchemy
- PostgreSQL 16
- Psycopg
- Pytest
- Pandas
- PyArrow
- Docker
- Docker Compose
- Git / GitHub

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── sources/
│   │   ├── cases.csv
│   │   ├── cases.json
│   │   └── cases.parquet
│   └── raw/
├── database/
│   ├── schema/
│   └── seeds/
├── docker/
│   └── init-db.sh
├── docs/
│   └── week2-data-pipeline.md
├── scripts/
│   ├── generate_parquet.py
│   └── load_curated_batch.py
├── src/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── exceptions/
│       ├── pipeline/
│       ├── repositories/
│       ├── schemas/
│       └── services/
├── tests/
├── compose.yaml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Week 1: Case Management Backend

The initial backend established the core application architecture.

### Database

The PostgreSQL schema contains the main commerce and case-management entities:

- Customers
- Vendors
- Products
- Vendor Products
- Orders
- Order Items
- Payments
- Vendor Payouts
- Delivery Persons
- Deliveries
- Delivery Attempts
- Returns
- Refunds
- Support Agents
- Cases
- Case Updates

The database is normalized to avoid unnecessary duplication. Foreign keys are used to preserve relationships between entities.

### API

Current API endpoints include:

```text
GET    /api/v1/health
POST   /api/v1/cases
GET    /api/v1/cases
GET    /api/v1/cases/{case_id}
PATCH  /api/v1/cases/{case_id}
```

Interactive API documentation is available through FastAPI/OpenAPI at:

```text
http://localhost:8000/docs
```

## Week 2: Enterprise Data Pipeline

Week 2 introduces a production-oriented data ingestion pipeline capable of processing heterogeneous source formats.

### Supported source formats

- CSV
- JSON
- Parquet

Each source can represent the same business concept using different field names and structures. Source-specific adapters read the native representation, while explicit source mappings convert records into one standardized contract.

### Standardized data contract

All valid case records are converted into the following conceptual structure:

```text
case_id
actor_type
actor_id
case_type
priority
status
category
description
created_at
```

The contract uses strict validation so downstream pipeline stages do not need to understand every source format.

### Raw layer

Original source files are preserved before transformation. Each raw batch stores metadata including:

- Source name
- Batch ID
- Original filename
- Stored path
- Ingestion timestamp
- File size
- SHA-256 checksum

This supports auditability, replay, and troubleshooting.

### Quality and quarantine

Schema/type correctness is handled by the standardized contract. Dataset-level quality checks handle issues such as duplicate case IDs within a batch.

Rejected records are stored in `pipeline_quarantine` together with the original record and quality issues.

### Curated layer

Valid records are written to `curated_cases` in PostgreSQL.

The table has a unique constraint on:

```text
(source_name, case_id)
```

This provides a database-level idempotency guardrail.

### Incremental processing

The pipeline first checks which case IDs for a source have already been curated. Existing records can therefore be skipped before attempting persistence.

Incremental filtering improves efficiency.

The database unique constraint provides the final correctness guarantee even if application-level filtering is bypassed or races occur.

### Reconciliation

Each pipeline batch verifies that all source records are accounted for:

```text
source records
    = standardized records
    = rejected records
      + already-present records
      + newly persisted records
```

A reconciliation failure causes the pipeline to fail rather than silently accepting an incomplete batch.

### Audit metadata

Every pipeline execution is recorded in `pipeline_runs` with information such as:

- Run ID
- Source name
- Batch ID
- Status
- Start/completion timestamps
- Source count
- Standardized count
- Rejected count
- Already-present count
- Persisted count
- Error message when applicable

## Docker Setup

Docker Compose runs the environment as multiple services:

```text
postgres   -> PostgreSQL database
app        -> FastAPI application
 db-init   -> one-shot database initialization job
```

Inside the Compose network, the application connects to PostgreSQL using the service name `postgres` rather than `localhost`.

### Prerequisites

Install:

- Docker Desktop
- Docker Compose (included with current Docker Desktop installations)

### Build the application image

```powershell
docker compose build
```

### Start PostgreSQL

```powershell
docker compose up -d postgres
```

### Initialize the database

On a fresh database volume:

```powershell
docker compose run --rm db-init
```

The initialization job applies the SQL schema files and loads the demo seed data.

### Start the API

```powershell
docker compose up -d app
```

Check service status:

```powershell
docker compose ps
```

Health endpoint:

```text
http://localhost:8000/api/v1/health
```

OpenAPI documentation:

```text
http://localhost:8000/docs
```

### Run the pipeline inside Docker

```powershell
docker compose run --rm app python scripts/load_curated_batch.py
```

## Pipeline Verification

The Dockerized pipeline was executed twice using the same source batch.

### First run

```text
Source records: 3
Rejected: 0
Already present: 0
Newly persisted: 3
```

### Second run

```text
Source records: 3
Rejected: 0
Already present: 3
Newly persisted: 0
```

The second execution did not create duplicates, demonstrating the intended incremental/idempotent behavior.

The PostgreSQL `pipeline_runs` table recorded both executions with `SUCCESS` status.

## Running Tests

Install development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Run the complete test suite:

```powershell
pytest
```

The project includes unit, API, repository, integration, and pipeline tests.

## CI

GitHub Actions runs the automated test workflow with PostgreSQL available as a service dependency. The CI workflow installs the project with its development dependencies, runs the test suite, and performs a Python compilation check.

## Database Operations

Connect to the Docker PostgreSQL instance:

```powershell
docker compose exec postgres psql -U postgres -d ecommerce_dispute_resolution
```

Useful checks:

```sql
SELECT * FROM curated_cases ORDER BY case_id;

SELECT run_id,
       source_name,
       status,
       source_count,
       standardized_count,
       rejected_count,
       already_present_count,
       persisted_count
FROM pipeline_runs
ORDER BY started_at;
```

To completely reset the Docker database and its volume:

```powershell
docker compose down -v
```

Then recreate PostgreSQL and initialize it again.

> Warning: `docker compose down -v` deletes the Docker PostgreSQL volume and therefore removes the database data stored in that volume.

## Development Principles

The project follows a few core engineering principles:

1. Keep business responsibilities separated across API, service, repository, and pipeline layers.
2. Validate data early so downstream components can depend on explicit contracts.
3. Preserve source data before transformation.
4. Prefer deterministic and explainable transformations over implicit magic.
5. Make repeated pipeline execution safe.
6. Record enough metadata to explain what happened during every pipeline run.
7. Keep infrastructure reproducible through Docker.
8. Test behavior at unit, integration, and API boundaries.

## Current Status

### Completed

- Case-management PostgreSQL schema
- FastAPI case-management backend
- Layered application architecture
- Request validation and consistent errors
- Structured JSON logging
- Request ID middleware
- Automated tests
- CI workflow
- CSV/JSON/Parquet source adapters
- Standardized pipeline contract
- Raw data preservation
- Data quality checks
- Quarantine layer
- Curated layer
- Incremental processing
- Database-backed idempotency
- Reconciliation
- Pipeline audit metadata
- Docker image
- Docker Compose environment
- Dockerized pipeline execution

### Next

Week 3 introduces Retrieval-Augmented Generation (RAG):

```text
Knowledge documents
        ↓
Document loading
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector storage
        ↓
Retrieval
        ↓
LLM-generated grounded response
```

The RAG layer will complement PostgreSQL rather than replace it: PostgreSQL stores transactional facts, while the knowledge base stores unstructured organizational knowledge such as policies and procedures.
