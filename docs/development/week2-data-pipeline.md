# Week 2 — Enterprise Data Pipeline

## 1. Objective

Week 2 extends the case-management backend with an enterprise-style data pipeline.

The purpose is to take case records arriving from heterogeneous source systems, normalize them into a common representation, validate them, isolate bad records, persist trusted data into a curated PostgreSQL layer, and record enough metadata to audit every execution.

The pipeline is intentionally designed around five properties:

- **Source-agnostic:** downstream logic should not care whether data came from CSV, JSON, Parquet, or another source.
- **Incremental:** already-processed records should not be repeatedly processed when they do not need to be.
- **Idempotent:** rerunning the same batch must not create duplicate curated records.
- **Auditable:** each execution must leave enough metadata to understand what happened.
- **Reproducible:** the environment should be runnable consistently through Docker.

---

## 2. End-to-End Architecture

```text
                   Heterogeneous source systems
                    /          |          \
                   /           |           \
                CSV          JSON       Parquet
                  \             |            /
                   \            |           /
                    v           v          v
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
                       /        \
                      /          \
                     v            v
                  Valid         Rejected
                   data          records
                     |              |
                     |              v
                     |          Quarantine
                     |
                     v
              Incremental filter
                     |
                     v
              Curated PostgreSQL
                     |
                     v
                Reconciliation
                     |
                     v
                Pipeline audit
```

This design separates concerns. Reading a source is not the same thing as interpreting it, validation is not the same thing as persistence, and audit metadata should not be mixed with business records.

---

## 3. Why Heterogeneous Sources Matter

Enterprise systems rarely expose the same business data in exactly the same format.

For example, the same case ID may appear as:

```text
CSV:
case_id

JSON:
caseId

Parquet:
case_identifier
```

Likewise, a customer identifier could be named `customer_id` in one source and `customerId` in another.

If downstream code directly understands every source format, the system becomes tightly coupled to external systems.

Instead, the pipeline uses source adapters followed by explicit standardization.

The downstream pipeline sees one predictable contract.

---

## 4. Source Adapters

Source adapters are responsible for reading the native representation of a source.

Current adapters:

```text
src/app/pipeline/sources/
├── base.py
├── csv_source.py
├── json_source.py
└── parquet_source.py
```

Their responsibility is intentionally limited to source reading.

They do **not** contain business-level transformation logic.

Conceptually:

```python
raw_records = adapter.read_raw()
```

The result is a collection of source-native dictionaries.

This separation allows a new source type to be added without changing the standardization or curated-loading logic.

---

## 5. Standardized Data Contract

After source reading, records are converted into `StandardizedCaseRecord`.

The current contract contains:

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

The contract is implemented with Pydantic and uses strict field constraints and enumerated values where appropriate.

The model also rejects unexpected fields.

### Why a contract?

Without a contract, every downstream stage would need assumptions about source-specific field names and values.

With a contract:

```text
CSV  ────┐
JSON ────┼──> StandardizedCaseRecord ──> downstream logic
Parquet ┘
```

Downstream processing only needs to understand `StandardizedCaseRecord`.

### Contract vs. quality checks

These are intentionally different.

**Contract validation** answers:

> “Is this individual record structurally valid?”

Examples:

- Is `case_id` an integer?
- Is it positive?
- Is `priority` an allowed value?
- Is `created_at` a valid datetime?
- Are required fields present?

**Quality validation** answers:

> “Does this collection of records make sense as a dataset?”

Example:

- Are two records using the same `case_id` within the same batch?

Keeping these responsibilities separate avoids duplicate validation logic.

---

## 6. Explicit Source Mappings

The current implementation uses explicit mappings for each supported source.

Conceptually:

```text
CSV:
case_id        -> case_id
customer_id    -> actor_id
case_type      -> case_type
...

JSON:
caseId         -> case_id
customerId     -> actor_id
caseType       -> case_type
...

Parquet:
case_identifier -> case_id
actor_id        -> actor_id
...
```

This is deliberately deterministic.

The pipeline does not attempt to automatically guess arbitrary field names such as:

```text
Customer_ID
CustomerID
Cust_ID
customer_identifier
```

That kind of flexibility could be added later through aliases or configuration, but automatic fuzzy interpretation would introduce ambiguity and hidden failures. In an enterprise pipeline, predictable behavior is generally preferable to “clever” behavior.

---

## 7. Raw Layer

The raw layer preserves the original source file before transformations occur.

The implementation stores the original bytes along with metadata including:

```text
source_name
batch_id
original_filename
stored_path
ingested_at
size_bytes
sha256
```

### Why preserve raw data?

Suppose a downstream transformation contains a bug.

Without the original input, the team may have to ask the external system to resend data.

With the raw layer:

```text
original source
      |
      +----> transformation v1
      |
      +----> transformation v2
      |
      +----> audit/replay
```

This is useful for troubleshooting, replay, audit, and future reprocessing.

Raw data is stored below `data/raw/`, which is excluded from Git because it is runtime data rather than source code.

---

## 8. Data Quality

The quality layer currently focuses on dataset-level problems that are not already guaranteed to be caught by the contract.

The first implemented rule checks for duplicate `case_id` values inside a batch.

A quality result contains:

```text
valid_records
rejected_records
rejected_indexes
issues
```

This makes rejection explicit rather than silently dropping records.

---

## 9. Quarantine

Invalid records are persisted separately in `pipeline_quarantine`.

The quarantine record contains information such as:

```text
source_name
batch_id
record_index
raw_record
issue_codes
issue_messages
created_at
```

### Why quarantine instead of deletion?

The pipeline should not simply do:

```text
bad record -> disappear
```

Instead:

```text
bad record
    |
    v
quarantine
    |
    +--> inspect
    +--> correct upstream data
    +--> replay later
```

This keeps the main curated dataset clean while retaining the evidence needed to investigate failures.

---

## 10. Curated Layer

Trusted records are written to `curated_cases`.

This is the normalized, standardized representation suitable for downstream application and analytical use.

The current table stores fields including:

```text
curated_case_id
source_name
batch_id
case_id
actor_type
actor_id
case_type
priority
status
category
description
source_created_at
curated_at
```

The table has a unique constraint on:

```text
(source_name, case_id)
```

This constraint is an important correctness boundary.

---

## 11. Incremental Processing vs. Idempotency

These concepts are related but not identical.

### Incremental processing

The application first asks:

> “Which of these records are already present?”

Existing records can be skipped before persistence.

This primarily improves efficiency by avoiding unnecessary work.

### Idempotency

Idempotency asks:

> “What happens if the same operation is executed more than once?”

The database protects curated data with:

```text
UNIQUE(source_name, case_id)
```

and insertion uses PostgreSQL conflict handling so an already-present record is not inserted again.

Therefore:

```text
Application check
        |
        | performance optimization
        v
Database uniqueness
        |
        | correctness guarantee
        v
No duplicate curated record
```

The two mechanisms complement each other.

---

## 12. Reconciliation

A pipeline should not merely report “success” because no exception occurred.

It should verify that every source record is accounted for.

For this pipeline:

```text
source_count
    = standardized_count
```

and the source records must be explained by:

```text
rejected_count
+ already_present_count
+ persisted_count
```

Therefore:

```text
accounted_count =
    rejected_count
    + already_present_count
    + persisted_count
```

A reconciliation failure causes the pipeline to fail rather than silently accepting incomplete processing.

---

## 13. Pipeline Run Audit

Every pipeline execution receives a UUID `run_id` and is stored in `pipeline_runs`.

The run record captures:

```text
run_id
source_name
batch_id
status
started_at
completed_at
source_count
standardized_count
rejected_count
already_present_count
persisted_count
error_message
```

### Transaction design

The audit record is intentionally handled so that a failed business transaction does not erase the evidence that the run failed.

The general flow is:

```text
Create RUNNING audit record
          |
          v
Commit audit transaction
          |
          v
Execute pipeline work
       /       \
      /         \
 success       failure
    |              |
    v              v
Complete        Rollback business work
SUCCESS         |
    |           v
    v       New audit transaction
  Commit         |
                 v
             Mark FAILED
                 |
               Commit
```

This is an important enterprise pattern: operational metadata should remain available even when the business transaction fails.

---

## 14. End-to-End Pipeline Execution

The main execution script is:

```text
scripts/load_curated_batch.py
```

The flow is approximately:

```text
1. Create database session
2. Start audit run
3. Read source records
4. Standardize records
5. Run quality checks
6. Store rejected records in quarantine
7. Identify already-present records
8. Insert new records into curated_cases
9. Reconcile counts
10. Mark audit run SUCCESS
```

If an exception occurs, business changes are rolled back and the audit run is recorded as `FAILED`.

---

## 15. Docker Architecture

Docker Compose defines three services:

```text
              +----------------+
              |      app       |
              |    FastAPI     |
              +-------+--------+
                      |
                      | postgres:5432
                      v
              +----------------+
              |    postgres    |
              | PostgreSQL 16  |
              +----------------+

              +----------------+
              |    db-init     |
              | one-shot job   |
              +-------+--------+
                      |
                      v
                postgres schema
                 + seed data
```

### Why Compose?

The application and database are separate services but need to work together.

Compose provides:

- A reproducible multi-container environment.
- Service discovery by service name.
- Dependency management.
- Shared networking.
- Persistent PostgreSQL storage through a named volume.

Inside the Compose network, the API uses:

```text
postgres:5432
```

The host machine accesses the API through:

```text
localhost:8000
```

---

## 16. Database Initialization

`docker/init-db.sh` is used by the one-shot `db-init` service.

It waits for PostgreSQL to become ready, applies the SQL schema files in order, and then loads the demo seed data.

The initialization flow is:

```text
PostgreSQL healthy
       |
       v
Apply schema/001...019
       |
       v
Load demo seed data
       |
       v
Database ready
```

The initialization workflow is intended for a fresh database volume.

To completely reset the Docker database:

```powershell
docker compose down -v
```

Then recreate PostgreSQL and run the initialization service again.

> `docker compose down -v` removes the named PostgreSQL volume and therefore deletes the database data stored in that volume.

---

## 17. Verification Performed

The pipeline was executed from the Dockerized application container twice using the same source batch `week2-csv-001`.

### First execution

```text
Pipeline run successful.
Source records: 3
Rejected: 0
Already present: 0
Newly persisted: 3
```

Audit result:

```text
status               SUCCESS
source_count         3
standardized_count   3
rejected_count       0
already_present      0
persisted_count      3
```

### Second execution

The exact same command was executed again.

```text
Pipeline run successful.
Source records: 3
Rejected: 0
Already present: 3
Newly persisted: 0
```

Audit result:

```text
status               SUCCESS
source_count         3
standardized_count   3
rejected_count       0
already_present      3
persisted_count      0
```

### Curated result

The curated database contained the expected records:

```text
source_name   case_id   status
-----------   -------   ------------
csv           101       OPEN
csv           102       IN_PROGRESS
csv           103       OPEN
```

This verifies that:

- Source ingestion works.
- Standardization works.
- Quality checks passed.
- Curated persistence works.
- Incremental filtering detects already-present records.
- Rerunning the same batch does not create duplicates.
- Pipeline audit records both runs.
- The pipeline works from the Dockerized application environment.

---

## 18. Tests

The project contains tests across multiple layers:

```text
Unit tests
  -> individual pipeline and application components

API tests
  -> FastAPI request/response behavior

Repository tests
  -> database persistence behavior

Integration tests
  -> multi-component database behavior

Pipeline tests
  -> source -> standardization -> quality -> curated flow
```

The full test suite has been run successfully with **56 tests passing** before the final Docker verification stage. The known non-blocking warnings come from dependency deprecations in the FastAPI/Starlette test client stack and are intentionally being deferred.

Run the suite with:

```powershell
pytest
```

---

## 19. CI

The GitHub Actions workflow uses PostgreSQL as a service dependency and performs the automated project checks.

The CI flow installs the package with development dependencies, initializes the database as required by the tests, runs the test suite, and performs Python compilation checks.

Docker is used for local environment reproducibility in Week 2. Broader CI/CD containerization and deployment are part of later engineering work.

---

## 20. Engineering Decisions

### PostgreSQL instead of SQLite

PostgreSQL was selected because the system models an enterprise case-management domain and requires reliable relational constraints, JSONB storage, transactional behavior, and production-oriented database semantics.

### SQL schema as authoritative

The SQL schema is maintained explicitly rather than relying on automatic ORM table creation. This makes database structure visible, reviewable, and reproducible.

### `ON DELETE RESTRICT`

Core entities should not disappear accidentally while dependent business records still refer to them. Restrictive foreign-key behavior makes destructive operations explicit.

### Explicit mappings rather than fuzzy matching

Source field interpretation is deterministic and reviewable. More flexible alias/configuration mechanisms can be introduced later if the number of source variants justifies them.

### Separate application and audit transactions

Operational audit information should survive a failed business transaction.

### Runtime raw data is not committed to Git

`data/raw/` is ignored because raw ingested files are runtime artifacts and may become large or sensitive.

---

## 21. Operational Commands

### Build

```powershell
docker compose build
```

### Start PostgreSQL

```powershell
docker compose up -d postgres
```

### Initialize database

```powershell
docker compose run --rm db-init
```

### Start API

```powershell
docker compose up -d app
```

### Check services

```powershell
docker compose ps
```

### Run pipeline

```powershell
docker compose run --rm app python scripts/load_curated_batch.py
```

### Open PostgreSQL shell

```powershell
docker compose exec postgres psql -U postgres -d ecommerce_dispute_resolution
```

### Run tests locally

```powershell
pytest
```

### Stop services without deleting database data

```powershell
docker compose down
```

### Stop services and delete the PostgreSQL volume

```powershell
docker compose down -v
```

---

## 22. Completion Criteria for Week 2

Week 2 is considered complete when the following are true:

- [x] Multiple heterogeneous source formats are supported.
- [x] A standardized data contract exists.
- [x] Raw source preservation is implemented.
- [x] Data-quality checks are implemented.
- [x] Invalid records can be quarantined.
- [x] Valid records are loaded into a curated layer.
- [x] Incremental processing is implemented.
- [x] Database-backed idempotency is enforced.
- [x] Reconciliation validates batch accounting.
- [x] Pipeline execution is auditable.
- [x] Docker image builds successfully.
- [x] Docker Compose environment works.
- [x] Pipeline runs successfully inside Docker.
- [x] Repeating the same batch produces zero new curated records.
- [x] Documentation covers setup, architecture, operation, and design decisions.

The next stage is Week 3: Retrieval-Augmented Generation.
