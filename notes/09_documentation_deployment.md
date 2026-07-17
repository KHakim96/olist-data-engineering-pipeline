# Phase 09 — Documentation & Deployment

## Objective

Finalize the project for public release by completing documentation, preparing the repository, deploying the Streamlit dashboard, and publishing the project to GitHub.

---

# Tasks Completed

## 1. Completed Project Documentation

Created and updated the following documentation.

- README.md
- docs/profiling_report.md
- docs/key_validation_report.md
- docs/parquet_export_report.md
- docs/duckdb_load_report.md
- docs/testing/testing_summary.md
- docs/architecture.md

---

## 2. Created Architecture Diagram

Documented the complete end-to-end data engineering architecture using Mermaid.

Pipeline:

Raw CSV
→ PostgreSQL
→ Parquet Data Lake
→ DuckDB Warehouse
→ dbt
→ Analytics Marts
→ Streamlit Dashboard

This diagram is included in the project documentation and README.

---

## 3. Repository Cleanup

Removed unnecessary files before publishing.

Deleted:

- docker-compose.official.yml
- Temporary logs
- __pycache__
- dbt target folder
- dbt logs
- Airflow runtime files
- Temporary testing files

Cleaned .gitignore to exclude generated files while keeping required project assets.

---

## 4. Updated dbt Configuration

Modified profiles.yml to remove the Docker-specific database path.

Before

path:
/opt/airflow/warehouse/olist.duckdb

After

path:
../warehouse/olist.duckdb

Benefits

- Works locally
- Works in Docker
- Works on Streamlit Cloud
- Removes hardcoded environment dependency

---

## 5. Streamlit Deployment

Initially deployed the dashboard to Streamlit Community Cloud.

The application started successfully, but every dashboard page failed because the DuckDB warehouse database was missing.

Error

IO Error:
Cannot open warehouse/olist.duckdb

---

## 6. Deployment Investigation

Several deployment approaches were evaluated.

### Attempt 1

Automatically rebuild DuckDB at application startup.

Result

Partially successful.

The warehouse could be rebuilt, but dbt models required additional initialization and significantly complicated the deployment.

Decision

Rejected.

---

### Attempt 2

Automatically execute:

- load_duckdb.py
- dbt run

before loading Streamlit.

Although functional, this introduced unnecessary complexity into the dashboard startup.

Decision

Rejected.

---

### Final Solution

Discovered the completed DuckDB warehouse size was approximately 93 MB.

GitHub permits files smaller than 100 MB.

Instead of rebuilding the warehouse during deployment, the finished warehouse database was committed directly into the repository.

Advantages

- Simple deployment
- Faster application startup
- No initialization logic
- No duplicated pipeline code
- Cleaner architecture

---

## 7. Updated Git Ignore Rules

Modified .gitignore.

Before

warehouse/

After

warehouse/*
!warehouse/olist.duckdb

This allows only the production warehouse database to be committed while ignoring any future temporary files.

---

## 8. Published to GitHub

Successfully pushed the complete project.

Repository

https://github.com/KHakim96/olist-data-engineering-pipeline

GitHub generated a warning because the DuckDB database is larger than 50 MB.

Database size

Approximately 93 MB

The file is below GitHub's hard 100 MB limit and was accepted successfully.

---

## 9. Streamlit Deployment Success

After pushing the final repository, the application was redeployed.

Deployment succeeded.

Verified dashboards

- Executive Dashboard
- Sales Dashboard
- Customers Dashboard
- Products Dashboard
- Delivery Dashboard
- Reviews Dashboard
- Geography Dashboard

All dashboards successfully query the production DuckDB warehouse.

---

# Final Architecture

Raw CSV Files

↓

PostgreSQL

↓

Parquet Data Lake

↓

DuckDB Warehouse

↓

dbt
(Staging → Intermediate → Marts)

↓

Streamlit Dashboard

↓

Business Users

---

# Project Status

Project Planning

Completed

Project Setup

Completed

PostgreSQL Ingestion

Completed

Parquet Data Lake

Completed

DuckDB Warehouse

Completed

dbt Transformations

Completed

Airflow Pipeline

Completed

Analytics Dashboard

Completed

Testing & Data Quality

Completed

Documentation & Deployment

Completed

---

# Final Deliverables

✔ Complete Data Engineering Pipeline

✔ PostgreSQL ETL

✔ Parquet Data Lake

✔ DuckDB Analytics Warehouse

✔ dbt Data Models

✔ Apache Airflow Orchestration

✔ Streamlit Dashboard

✔ Automated Tests

✔ Documentation

✔ GitHub Repository

✔ Live Streamlit Deployment

---

# Lessons Learned

- Design documentation before implementation.
- Separate raw, staging, intermediate, and mart layers.
- Use Parquet as the analytical data lake.
- Keep dbt responsible for business transformations.
- DuckDB provides excellent performance for analytical workloads.
- Streamlit Community Cloud can successfully host a production analytics dashboard using DuckDB.
- Simpler deployment architecture is preferable when it satisfies project requirements.