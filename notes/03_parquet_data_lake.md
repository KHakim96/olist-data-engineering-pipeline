# Phase 3 - Parquet Data Lake

---

# Objective

The objective of this phase is to transform the PostgreSQL relational database into a modern analytics-ready Data Lake using the Apache Parquet file format.

Instead of querying PostgreSQL directly for analytical workloads, the data is exported into compressed Parquet files. These files become the foundation for the next phase, where DuckDB will be used as the analytical data warehouse.

This phase also introduces the concept of a Data Lake, where structured data is stored as files rather than inside a database.

---

# Why This Phase Exists

During Phase 2, all Olist CSV datasets were successfully loaded into PostgreSQL.

Although PostgreSQL is excellent for transactional storage and relational integrity, it is not the optimal format for analytical processing.

Modern data engineering pipelines usually separate:

- Operational Storage
- Analytical Storage

Instead of querying the operational database directly, data is exported into a Data Lake.

Benefits include:

- Faster analytical queries
- Smaller storage footprint
- Columnar storage
- Better compression
- Easier integration with modern data warehouses

For this project, Apache Parquet was selected as the Data Lake storage format.

---

# What is Apache Parquet?

Apache Parquet is an open-source columnar storage file format maintained by the Apache Software Foundation.

Unlike CSV files, which store data row by row, Parquet stores data column by column.

Example:

Traditional CSV

CustomerID | Name | City | State
--------------------------------
1          | Ali  | KL   | Selangor

Stored as:

CustomerID,Name,City,State
1,Ali,KL,Selangor

Every query scans every column.

--------------------------------------------

Apache Parquet

CustomerID Column
-----------------
1
2
3

Name Column
-----------
Ali
John
Sara

City Column
-----------
KL
Penang
Johor

Only required columns are read during queries.

This significantly improves analytical performance.

---

# Why Use Parquet?

Advantages of Apache Parquet include:

- Columnar storage
- High compression
- Smaller file size
- Faster analytical queries
- Better compatibility with modern analytics engines
- Native support by DuckDB, Spark, Snowflake, BigQuery, Athena and Databricks

Because of these advantages, Parquet has become one of the industry standards for Data Lakes.

---

# What is a Data Lake?

A Data Lake is a centralized storage layer that stores data as files rather than inside relational databases.

Instead of:

CSV
↓

PostgreSQL

the architecture becomes:

CSV
↓

PostgreSQL
↓

Parquet Files

The Parquet files become the Data Lake.

In production environments these files are usually stored inside:

- Amazon S3
- Azure Data Lake Storage (ADLS)
- Google Cloud Storage (GCS)
- MinIO

For this project, the Data Lake is stored locally inside:

data/processed/

This simulates a real-world Data Lake architecture while remaining lightweight and portable.

---

# Phase 3 Architecture

The overall architecture after completing Phase 3 is shown below.

```text
                        OLIST DATA ENGINEERING PIPELINE

                    Raw CSV Files
                          │
                          ▼
                 PostgreSQL Database
                          │
                          ▼
                export_parquet.py
                          │
                          ▼
               Apache Parquet Files
                          │
                          ▼
                  data/processed/
                          │
                          ▼
          DuckDB Data Warehouse (Next Phase)
```

The export process transforms relational tables inside PostgreSQL into compressed Parquet files that will later be loaded into DuckDB.

---

# End-to-End Export Flow

The complete workflow executed during this phase is illustrated below.

```text
Connect to PostgreSQL
        │
        ▼
Read Table
        │
        ▼
Load into Pandas DataFrame
        │
        ▼
Export DataFrame to Parquet
        │
        ▼
Measure File Size
        │
        ▼
Store Export Metadata
        │
        ▼
Generate Markdown Report
        │
        ▼
Print Export Summary
```

Each table follows exactly the same pipeline.

This keeps the code reusable and makes adding new tables straightforward.

---

# Folder Structure

Before exporting, the project contains only the raw CSV datasets.

```text
data/

├── raw/
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   └── ...
│
└── processed/
```

After Phase 3 completes successfully:

```text
data/

├── raw/
│
└── processed/
    ├── category_translation.parquet
    ├── customers.parquet
    ├── sellers.parquet
    ├── products.parquet
    ├── geolocation.parquet
    ├── orders.parquet
    ├── order_items.parquet
    ├── order_payments.parquet
    └── order_reviews.parquet
```

The `processed` directory now represents the project's Data Lake.

---

# Export Script

The main script responsible for this phase is:

```text
scripts/export/export_parquet.py
```

Its responsibilities include:

- Connecting to PostgreSQL
- Reading every table
- Exporting each table as Parquet
- Measuring exported file size
- Recording export metadata
- Generating an export report
- Printing execution summary

Instead of writing a separate script for every table, one reusable pipeline handles every dataset.

---

# Shared Dataset Configuration

Instead of manually defining every table inside the export script, the existing dataset configuration from Phase 2 is reused.

```text
scripts/
└── ingestion/
    └── datasets.py
```

The export script imports the dataset metadata:

```python
from scripts.ingestion.datasets import DATASETS
```

Then automatically creates the export list:

```python
TABLES = [
    dataset["table"]
    for dataset in DATASETS
]
```

This approach creates a single source of truth.

Whenever a new dataset is added, only `datasets.py` needs to be updated.

Every pipeline component automatically receives the updated table list.

---

# Why Reuse datasets.py?

Without a shared dataset configuration:

PostgreSQL

↓

Manual Table List

↓

Parquet

↓

Another Manual Table List

↓

DuckDB

↓

Another Manual Table List

Every phase would require maintaining duplicate lists.

Instead:

```text
datasets.py
       │
       ├────────► PostgreSQL Ingestion
       ├────────► Parquet Export
       ├────────► DuckDB Loader
       ├────────► Airflow DAG
       └────────► Future Testing
```

This greatly improves maintainability and reduces duplication throughout the project.

---

# Script Implementation

The entire export process is implemented inside:

```text
scripts/export/export_parquet.py
```

The script was designed using small reusable functions rather than placing all logic inside one large `main()` function.

This improves:

- Readability
- Maintainability
- Reusability
- Debugging
- Future scalability

The overall execution flow is shown below.

```text
main()

│

├── get_connection()

├── read_table()

├── export_table()

├── get_file_size()

├── generate_report()

└── print_summary()
```

Each function is responsible for a single task.

---

# Project Configuration

At the beginning of the script, several project paths are defined.

```python
BASE_DIR
PROCESSED_DIR
DOCS_DIR
REPORT_FILE
```

These paths allow the script to locate:

- Project root
- Processed data folder
- Documentation folder
- Markdown report location

Instead of hardcoding paths throughout the script, every location is managed from one place.

This makes future maintenance much easier.

---

# PostgreSQL Configuration

Database connection settings are loaded from environment variables.

```python
DB_CONFIG = {
    ...
}
```

Using environment variables provides several advantages.

- Keeps credentials outside the source code
- Easier deployment
- Docker compatibility
- Better security

The export script uses the same PostgreSQL database created during Phase 2.

---

# get_connection()

Purpose

Create a connection to PostgreSQL.

Workflow

```text
Read Environment Variables

↓

Connect to PostgreSQL

↓

Return Connection Object
```

If the connection fails, the exception is raised immediately so the export process stops before reading any tables.

---

# read_table()

Purpose

Read an entire PostgreSQL table into a Pandas DataFrame.

Workflow

```text
PostgreSQL

↓

SELECT *

↓

Pandas DataFrame
```

The function uses:

```python
pd.read_sql(...)
```

Advantages

- Simple implementation
- Direct DataFrame creation
- Easy integration with Pandas

Every exported table follows this same process.

---

# export_table()

Purpose

Convert a Pandas DataFrame into an Apache Parquet file.

Workflow

```text
DataFrame

↓

Create processed directory

↓

Write Parquet

↓

Return file path
```

The function automatically creates the destination folder if it does not already exist.

```python
PROCESSED_DIR.mkdir(...)
```

The exported filename follows a simple naming convention.

Example

```text
customers.parquet

orders.parquet

products.parquet
```

This naming convention keeps the Data Lake organized and predictable.

---

# Why Parquet?

Instead of exporting CSV files, the pipeline exports Apache Parquet.

Advantages include:

- Better compression
- Smaller storage size
- Faster analytical queries
- Columnar storage
- Native support by DuckDB

During this project:

Approximately

CSV
↓

120–150 MB

became

Parquet
↓

~55 MB

This demonstrates one of Parquet's biggest advantages.

---

# get_file_size()

Purpose

Calculate the size of every exported Parquet file.

Workflow

```text
Parquet File

↓

Read File Size

↓

Convert Bytes

↓

Return MB
```

The file size is later included inside the export report.

This provides visibility into storage usage and compression efficiency.

---

# Export Metadata

After every successful export, metadata is stored.

Each exported table records:

- Table name
- Number of rows
- Number of columns
- Output filename
- File size

Example

```text
customers

Rows:
99,441

Columns:
5

File:
customers.parquet

Size:
6.76 MB
```

This metadata is later used to generate the Markdown report.

---

# generate_report()

Purpose

Automatically generate a Markdown report summarizing the export process.

The report contains:

- Export timestamp
- Total tables exported
- Total rows exported
- Export summary table
- File sizes

Output location

```text
docs/

└── parquet_export_report.md
```

Instead of manually documenting every execution, the report is generated automatically after every successful export.

This makes pipeline execution reproducible and easy to audit.

---

# Main Pipeline

The `main()` function orchestrates the complete export process.

Instead of manually exporting individual tables, one loop processes every dataset automatically.

Execution flow:

```text
Start Export
      │
      ▼
Connect to PostgreSQL
      │
      ▼
Loop Through All Tables
      │
      ▼
Read Table
      │
      ▼
Export to Parquet
      │
      ▼
Calculate File Size
      │
      ▼
Store Export Metadata
      │
      ▼
Generate Markdown Report
      │
      ▼
Close Database Connection
      │
      ▼
Print Export Summary
```

This design makes the pipeline reusable and scalable.

Adding a new dataset only requires updating `datasets.py`.

No changes are required inside the export logic.

---

# Export Results

The export completed successfully.

Summary

| Metric | Value |
|---------|------:|
| Tables Exported | 9 |
| Total Rows | 1,551,698 |
| Failed Tables | 0 |
| Output Format | Apache Parquet |

Generated files

| Table | File |
|-------|------|
| Category Translation | category_translation.parquet |
| Customers | customers.parquet |
| Sellers | sellers.parquet |
| Products | products.parquet |
| Geolocation | geolocation.parquet |
| Orders | orders.parquet |
| Order Items | order_items.parquet |
| Order Payments | order_payments.parquet |
| Order Reviews | order_reviews.parquet |

Total Data Lake size

Approximately **55 MB**

This demonstrates the storage efficiency provided by Apache Parquet.

---

# Generated Report

Every successful execution automatically creates:

```text
docs/

└── parquet_export_report.md
```

The report contains:

- Export timestamp
- Total tables exported
- Total rows exported
- File sizes
- Output filenames

Example

```text
# Parquet Export Report

Generated:
2026-07-10

Tables Exported:
9

Total Rows:
1,551,698
```

Automated reporting improves reproducibility and provides an execution log for future reference.

---

# Validation

After the export completed, several validation checks were performed.

Validation Checklist

✅ All 9 PostgreSQL tables exported successfully

✅ All Parquet files created

✅ Total exported rows matched PostgreSQL

✅ Markdown report generated successfully

✅ No failed exports

These validation steps confirmed that the Data Lake was created successfully.

---

# Challenges Encountered

Several implementation issues were encountered during this phase.

## 1. Docker Volume Mapping

Initially, the Docker container only mounted the `scripts/` directory.

This caused inconsistencies between the local project structure and the container structure.

Solution

The Docker volume mapping was updated to mount the entire project.

```yaml
volumes:
  - ./:/opt/airflow
```

Benefits

- Consistent project structure
- Easier navigation
- Simpler imports
- Better maintainability

---

## 2. Python Package Imports

The export script initially failed with

```text
ModuleNotFoundError:
No module named 'scripts'
```

Cause

Python executed the script as a standalone file rather than as a package.

Solution

The `scripts` directory was converted into a Python package.

Empty `__init__.py` files were added.

The script is now executed using

```bash
python -m scripts.export.export_parquet
```

This allows absolute imports such as

```python
from scripts.ingestion.datasets import DATASETS
```

to work correctly.

---

## 3. Markdown Table Formatting

The generated Markdown report initially displayed an incorrectly formatted table.

Cause

Table rows were not formatted consistently.

Solution

The report generation logic was updated to produce valid Markdown tables.

The final report renders correctly on GitHub and Markdown viewers.

---

# Lessons Learned

This phase introduced several important data engineering concepts.

Topics learned

- Apache Parquet
- Data Lake architecture
- Columnar storage
- File compression
- Pandas Parquet export
- PostgreSQL extraction
- Automated report generation
- Python package structure
- Docker volume mapping
- Project organization

These concepts are commonly used in modern cloud-based data platforms.

---

# Phase Summary

Phase 3 successfully transformed the PostgreSQL database into a compressed Parquet Data Lake.

Pipeline after Phase 3

```text
Raw CSV
      │
      ▼
PostgreSQL
      │
      ▼
Parquet Data Lake
      │
      ▼
DuckDB Data Warehouse (Next Phase)
```

The project now has a reliable analytical storage layer that is significantly smaller and more efficient than the original CSV files.

This Data Lake will serve as the input for Phase 4, where all Parquet files will be loaded into DuckDB to build the project's analytical data warehouse.