# Phase 08 — Testing & Data Quality

## Objective

The objective of this phase was to validate every stage of the Olist Data Engineering Pipeline to ensure data integrity, correctness, and reliability before deployment.

Rather than only testing Python functions, this phase focused on validating the outputs produced by each pipeline stage.

---

# Pipeline Validation Scope

The following pipeline stages were validated:

```
Raw CSV
      │
      ▼
PostgreSQL
      │
      ▼
Parquet Data Lake
      │
      ▼
DuckDB Warehouse
      │
      ▼
dbt Analytics Models
      │
      ▼
Business Validation
```

---

# Testing Strategy

The testing strategy was divided into four independent stages.

| Test File | Purpose |
|-----------|---------|
| test_ingestion.py | Validate raw data ingestion |
| test_export_parquet.py | Validate Parquet export |
| test_load_duckdb.py | Validate DuckDB warehouse |
| test_pipeline.py | Validate end-to-end pipeline |

---

# Test 1 — Ingestion Validation

File

```
tests/test_ingestion.py
```

Purpose

Validate that the raw datasets are available and can be loaded correctly before entering PostgreSQL.

Implemented Tests

- Dataset configuration validation
- Raw data directory validation
- Dataset file existence
- CSV loading
- DataFrame validation
- Required column validation
- Customer ID validation
- Review score validation

Result

```
8 Tests Passed
```

---

# Test 2 — Parquet Export Validation

File

```
tests/test_export_parquet.py
```

Purpose

Validate that PostgreSQL tables are correctly exported into the Parquet Data Lake.

Implemented Tests

- Processed directory exists
- Parquet files exist
- Parquet files readable
- Parquet files not empty
- Row count validation

Result

```
5 Tests Passed
```

---

# Test 3 — DuckDB Warehouse Validation

File

```
tests/test_load_duckdb.py
```

Purpose

Validate that the warehouse contains all expected tables and business marts.

Implemented Tests

- DuckDB database exists
- Required tables exist
- Fact tables populated
- Dimension tables populated
- Executive dashboard mart exists
- Revenue KPI validation

Result

```
6 Tests Passed
```

---

# Test 4 — End-to-End Pipeline Validation

File

```
tests/test_pipeline.py
```

Purpose

Validate the complete analytics warehouse after the ETL pipeline has completed.

Implemented Tests

- Total orders
- Total customers
- Total products
- Total sellers
- Revenue validation
- Review score validation
- Duplicate order detection
- Orphan customer detection
- NULL order ID validation

Result

```
9 Tests Passed
```

---

# Test Results

| Test Suite | Tests |
|------------|------:|
| Ingestion | 8 |
| Parquet Export | 5 |
| DuckDB Warehouse | 6 |
| End-to-End Pipeline | 9 |

Total

```
28 Tests
```

Result

```
28 Passed
0 Failed
```

Success Rate

```
100%
```

---

# Major Issue Discovered

During the Parquet validation stage, the following test failed:

```
assert len(raw_df) == len(parquet_df)
```

The geolocation dataset returned:

Raw CSV

```
1,000,163 rows
```

Parquet

```
2,000,326 rows
```

Initially, the Parquet export script was suspected.

However, investigation showed that the export script simply exported data from PostgreSQL without modification.

Further investigation inside PostgreSQL confirmed:

```
SELECT COUNT(*)
FROM geolocation;
```

Result

```
2,000,326
```

This confirmed that the duplication occurred during the ingestion stage rather than the export stage.

---

# Root Cause Analysis

The ingestion pipeline inserted data using:

```
INSERT INTO table_name
```

without removing existing records.

As a result, rerunning the ingestion pipeline appended data into existing tables.

Pipeline execution

Run 1

```
1,000,163 rows
```

Run 2

```
2,000,326 rows
```

The pipeline was therefore not idempotent.

---

# Initial Attempt

The first implementation attempted to solve the problem by truncating each table inside the insert function.

Example

```
TRUNCATE TABLE table_name
```

before every insert.

This approach immediately failed.

PostgreSQL returned:

```
cannot truncate a table referenced in a foreign key constraint
```

because parent tables were truncated while child tables still referenced them.

---

# Final Solution

The ingestion pipeline was redesigned.

A dedicated function was introduced:

```
truncate_tables()
```

This function executes once before ingestion begins.

```
TRUNCATE TABLE

order_reviews,
order_payments,
order_items,
orders,
products,
sellers,
customers,
geolocation,
category_translation

RESTART IDENTITY CASCADE;
```

Pipeline execution now becomes:

```
Connect PostgreSQL

↓

Clear Existing Tables

↓

Load CSV Files

↓

Insert into PostgreSQL

↓

Export Parquet

↓

Load DuckDB

↓

Run dbt

↓

Analytics Dashboard
```

---

# Benefits

The pipeline is now idempotent.

Running the ingestion multiple times always produces identical database contents.

Example

Before

```
Run 1

1,000,163 rows

Run 2

2,000,326 rows
```

After

```
Run 1

1,000,163 rows

Run 2

1,000,163 rows
```

This behaviour is expected for batch ETL pipelines.

---

# Automated Test Reports

Each test suite generates its own report.

Commands

```
python -m pytest tests/test_ingestion.py -v \
> docs/testing/ingestion_test_results.txt

python -m pytest tests/test_export_parquet.py -v \
> docs/testing/export_parquet_test_results.txt

python -m pytest tests/test_load_duckdb.py -v \
> docs/testing/duckdb_test_results.txt

python -m pytest tests/test_pipeline.py -v \
> docs/testing/pipeline_test_results.txt
```

The generated reports are stored under:

```
docs/testing/
```

---

# Deliverables

Created

```
tests/

test_ingestion.py

test_export_parquet.py

test_load_duckdb.py

test_pipeline.py
```

Generated

```
docs/testing/

ingestion_test_results.txt

export_parquet_test_results.txt

duckdb_test_results.txt

pipeline_test_results.txt

testing_summary.md
```

---

# Phase Summary

Phase 08 successfully validated every major stage of the Olist Data Engineering Pipeline.

The testing process uncovered a critical idempotency issue within the PostgreSQL ingestion process. The issue was investigated, the root cause identified, and the ingestion pipeline redesigned to clear existing tables before loading new data.

After implementing the fix, all automated tests passed successfully.

Final Result

```
28 Tests Passed

0 Failed

100% Success Rate
```

The pipeline is now fully validated and ready to proceed to the documentation phase.