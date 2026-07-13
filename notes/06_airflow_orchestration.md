# Phase 6 — Airflow Orchestration

## Objective

The objective of this phase is to orchestrate the entire Olist Data Engineering Pipeline using Apache Airflow.

Instead of manually executing every ETL script, Airflow manages the complete workflow, ensuring every task runs in the correct sequence with dependency management, monitoring, retries, logging, and scheduling.

---

# Pipeline Architecture

```
Raw CSV Files
      │
      ▼
Profile Dataset
      │
      ▼
Verify Primary & Foreign Keys
      │
      ▼
Load PostgreSQL
      │
      ▼
Export Parquet Data Lake
      │
      ▼
Load DuckDB Data Warehouse
      │
      ▼
dbt Run
      │
      ▼
dbt Test
      │
      ▼
dbt Docs Generate
      │
      ▼
Pipeline Complete
```

---

# Technologies Used

- Apache Airflow
- Docker
- Python
- PostgreSQL
- DuckDB
- dbt
- BashOperator
- EmptyOperator

---

# DAG File

```
dags/olist_pipeline.py
```

---

# DAG Configuration

```python
with DAG(
    dag_id="olist_data_engineering_pipeline",
    description="End-to-end Olist Data Engineering Pipeline",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=[
        "olist",
        "data-engineering",
        "postgresql",
        "parquet",
        "duckdb",
        "dbt",
    ],
)
```

## Explanation

- Manual trigger pipeline
- No automatic schedule
- No historical backfill
- Retry failed tasks twice
- DAG grouped using descriptive tags

---

# Default Arguments

```python
default_args = {
    "owner": "Luqman",
    "depends_on_past": False,
    "retries": 2,
}
```

---

# Operators Used

## EmptyOperator

Used for pipeline boundaries.

```
start
end
```

---

## BashOperator

Used for executing every Python and dbt command.

Tasks executed:

- profile_dataset
- verify_keys
- load_postgresql
- export_parquet
- load_duckdb
- dbt_run
- dbt_test
- dbt_docs

---

# Commands Executed

```python
COMMANDS = {

"profile":
"python /opt/airflow/scripts/utilities/profile_dataset.py",

"verify":
"python /opt/airflow/scripts/utilities/verify_keys.py",

"postgres":
"python /opt/airflow/scripts/ingestion/ingest_postgres.py",

"parquet":
"PYTHONPATH=/opt/airflow python /opt/airflow/scripts/export/export_parquet.py",

"duckdb":
"PYTHONPATH=/opt/airflow python /opt/airflow/scripts/warehouse/load_duckdb.py",

"dbt_run":
"cd /opt/airflow/dbt_olist && dbt run",

"dbt_test":
"cd /opt/airflow/dbt_olist && dbt test",

"dbt_docs":
"cd /opt/airflow/dbt_olist && dbt docs generate",

}
```

---

# Working Directory

Every BashOperator executes using

```python
cwd="/opt/airflow"
```

This guarantees every script runs from the project root.

Without this configuration, Airflow executes tasks from a temporary working directory under `/tmp`, causing relative file paths to fail.

---

# Task Dependencies

```
start
    │
    ▼
profile_dataset
    │
    ▼
verify_keys
    │
    ▼
load_postgresql
    │
    ▼
export_parquet
    │
    ▼
load_duckdb
    │
    ▼
dbt_run
    │
    ▼
dbt_test
    │
    ▼
dbt_docs
    │
    ▼
end
```

Implemented as

```python
(
    start
    >> profile_dataset
    >> verify_keys
    >> load_postgresql
    >> export_parquet
    >> load_duckdb
    >> dbt_run
    >> dbt_test
    >> dbt_docs
    >> end
)
```

---

# Airflow Tasks

## profile_dataset

Runs

```
profile_dataset.py
```

Produces

```
docs/profiling_report.md
```

---

## verify_keys

Runs

```
verify_keys.py
```

Produces

```
docs/key_validation_report.md
```

---

## load_postgresql

Loads all raw CSV files into PostgreSQL.

---

## export_parquet

Exports PostgreSQL tables into

```
data/processed/*.parquet
```

Produces

```
docs/parquet_export_report.md
```

---

## load_duckdb

Loads all Parquet files into

```
warehouse/olist.duckdb
```

Produces

```
docs/duckdb_load_report.md
```

---

## dbt_run

Executes

```
dbt run
```

Builds

- Staging Models
- Intermediate Models
- Dimension Tables
- Fact Tables
- Executive Dashboard

Total models

```
26
```

---

## dbt_test

Executes

```
dbt test
```

Result

```
32 Tests Passed
```

---

## dbt_docs

Executes

```
dbt docs generate
```

Produces

```
manifest.json
catalog.json
index.html
```

---

# Debugging & Issues Encountered

## Issue 1

Problem

```
DAG would not execute.
```

Cause

```
start_date was in the future.
```

Solution

```python
start_date=datetime(2026,7,1)
```

---

## Issue 2

Problem

```
docs/profiling_report.md

FileNotFoundError
```

Cause

Airflow executed tasks from a temporary directory.

Solution

Added

```python
cwd="/opt/airflow"
```

to every BashOperator.

---

## Issue 3

Problem

```
ModuleNotFoundError

No module named scripts
```

Cause

Python package root not found during Airflow execution.

Solution

Updated commands

```bash
PYTHONPATH=/opt/airflow python ...
```

for

- export_parquet.py
- load_duckdb.py

---

## Issue 4

Problem

Airflow UI showed successful DAG run but no task execution.

Cause

Scheduler loaded an old DAG version before code changes.

Solution

Updated DAG, refreshed scheduler, and re-triggered DAG.

---

# Validation

Every task was tested individually using

```bash
airflow tasks test
```

Example

```bash
airflow tasks test \
olist_data_engineering_pipeline \
profile_dataset \
2026-07-13
```

Every task completed successfully before executing the complete pipeline.

---

# Final Airflow UI Result

Pipeline completed successfully.

```
Start

↓

Profile Dataset

↓

Verify Keys

↓

Load PostgreSQL

↓

Export Parquet

↓

Load DuckDB

↓

dbt Run

↓

dbt Test

↓

dbt Docs

↓

End
```

All tasks finished with SUCCESS status.

---

# Deliverables

Created

```
dags/
    olist_pipeline.py
```

Generated

```
docs/

profiling_report.md

key_validation_report.md

parquet_export_report.md

duckdb_load_report.md
```

Generated dbt artifacts

```
manifest.json

catalog.json

index.html
```

---

# Phase 6 Outcome

Successfully orchestrated the complete Olist Data Engineering Pipeline using Apache Airflow.

The workflow now executes automatically from raw CSV ingestion through data profiling, validation, PostgreSQL loading, Parquet export, DuckDB warehouse loading, dbt transformations, data quality testing, and documentation generation.

The pipeline supports dependency management, retry handling, centralized logging, task monitoring, and visual workflow execution through the Airflow web interface.