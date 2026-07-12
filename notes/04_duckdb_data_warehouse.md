# Phase 4 - DuckDB Data Warehouse

---

# Objective

The objective of this phase is to build an analytical Data Warehouse using DuckDB.

During Phase 3, all PostgreSQL tables were exported into Apache Parquet files and stored inside the project's Data Lake.

In this phase, those Parquet files are loaded into DuckDB to create a fast, lightweight analytical database that will serve as the foundation for dbt transformations and business analytics.

At the end of this phase, all analytical queries will be executed against DuckDB instead of PostgreSQL.

---

# Why This Phase Exists

The PostgreSQL database created in Phase 2 represents the operational database.

Its primary purpose is to store transactional data.

Although PostgreSQL can perform analytical queries, modern data engineering architectures usually separate operational databases from analytical databases.

Instead of running heavy reporting queries directly against PostgreSQL, the data is moved into a dedicated Data Warehouse.

This separation provides:

- Better analytical performance
- Reduced load on operational systems
- Faster reporting
- Better scalability
- Easier integration with BI tools

---

# What is a Data Warehouse?

A Data Warehouse is a database designed specifically for analytical workloads.

Unlike operational databases that process thousands of inserts and updates every second, a Data Warehouse is optimized for:

- Large SQL queries
- Aggregations
- Joins
- Reporting
- Dashboards
- Business Intelligence

Typical analytical questions include:

- Monthly revenue
- Top-selling products
- Customer lifetime value
- Average delivery time
- Sales by region

These queries scan millions of rows and are much more efficient in a warehouse than in an operational database.

---

# What is DuckDB?

DuckDB is an open-source analytical database management system (OLAP) designed for fast analytical queries.

Unlike PostgreSQL, DuckDB is an embedded database.

There is no separate database server.

Instead, the entire database is stored inside a single file.

For this project:

```text
warehouse/

└── olist.duckdb
```

This single file contains every analytical table.

DuckDB automatically manages:

- Storage
- Tables
- Metadata
- Query execution

without requiring a dedicated database server.

---

# Why DuckDB?

DuckDB offers several advantages for local analytics.

- Extremely fast analytical queries
- Native support for Apache Parquet
- Lightweight deployment
- No database server required
- Excellent SQL support
- Compatible with Pandas
- Compatible with dbt

Because of these features, DuckDB has become increasingly popular for local analytics, data engineering projects and modern ELT pipelines.

---

# Why Not Query PostgreSQL Directly?

Although PostgreSQL contains the same data, it serves a different purpose.

PostgreSQL is optimized for transactional processing.

Examples include:

- Customer purchases
- Order creation
- Payment processing
- Product updates

Running large analytical queries directly against PostgreSQL can negatively affect operational performance.

Instead, analytics are performed inside DuckDB while PostgreSQL remains the operational database.

---

# Why Load Parquet Instead of CSV?

The Parquet files created during Phase 3 already provide:

- Compressed storage
- Columnar format
- Optimized schema
- Analytics-ready data

Loading Parquet into DuckDB is significantly faster than loading the original CSV files.

The pipeline therefore becomes:

```text
CSV Files

↓

PostgreSQL

↓

Parquet Data Lake

↓

DuckDB Data Warehouse
```

This architecture closely mirrors modern cloud-based analytics platforms.

---

# Phase 4 Architecture

After completing this phase, the project architecture becomes:

```text
                Raw CSV Files
                       │
                       ▼
         PostgreSQL Operational Database
                       │
                       ▼
          Apache Parquet Data Lake
                       │
                       ▼
           DuckDB Data Warehouse
                       │
                       ▼
         dbt Transformations (Next Phase)
                       │
                       ▼
         Looker Studio Dashboard
```

DuckDB now becomes the primary analytical database for the remainder of the project.

---

# Phase 4 Architecture

The overall architecture after completing Phase 4 is illustrated below.

```text
                    OLIST DATA ENGINEERING PLATFORM

                     Raw CSV Files
                           │
                           ▼
              PostgreSQL Operational Database
                           │
                           ▼
                Apache Parquet Data Lake
                           │
                           ▼
              DuckDB Analytics Warehouse
                           │
                           ▼
                dbt Transformations
                     (Next Phase)
```

The DuckDB warehouse is built directly from the Parquet Data Lake.

This architecture separates operational storage from analytical processing and closely resembles modern cloud-based data engineering pipelines.

---

# End-to-End Warehouse Flow

The complete execution flow during this phase is shown below.

```text
Parquet Files
      │
      ▼
Connect to DuckDB
      │
      ▼
Create Warehouse Database
      │
      ▼
Load Parquet File
      │
      ▼
Create DuckDB Table
      │
      ▼
Validate Row Count
      │
      ▼
Store Summary Metadata
      │
      ▼
Generate Warehouse Report
      │
      ▼
Print Execution Summary
```

Each dataset follows the exact same process.

This allows the pipeline to scale easily whenever additional datasets are introduced.

---

# Folder Structure

Before Phase 4:

```text
warehouse/

(empty)
```

After completing Phase 4:

```text
warehouse/

└── olist.duckdb
```

This single database file now contains every analytical table.

The Data Lake remains unchanged.

```text
data/

├── raw/
│
└── processed/
    ├── customers.parquet
    ├── sellers.parquet
    ├── products.parquet
    ├── geolocation.parquet
    ├── orders.parquet
    ├── order_items.parquet
    ├── order_payments.parquet
    ├── order_reviews.parquet
    └── category_translation.parquet
```

The Parquet files continue serving as the storage layer, while DuckDB provides the analytics layer.

---

# Warehouse Database

Unlike PostgreSQL, DuckDB stores the entire database inside a single file.

Project structure:

```text
warehouse/

└── olist.duckdb
```

Inside this file:

```text
olist.duckdb

├── category_translation
├── customers
├── sellers
├── products
├── geolocation
├── orders
├── order_items
├── order_payments
└── order_reviews
```

Each table was automatically created from its corresponding Parquet file.

No manual table creation was required.

---

# Warehouse Loader

The entire warehouse creation process is implemented inside:

```text
scripts/

└── warehouse/

    └── load_duckdb.py
```

Responsibilities of this script include:

- Creating the warehouse directory
- Connecting to DuckDB
- Reading Parquet files
- Creating warehouse tables
- Validating row counts
- Recording warehouse metadata
- Generating a Markdown report
- Printing an execution summary

The script is fully reusable and automatically processes every dataset defined by the project configuration.

---

# Shared Dataset Configuration

Instead of manually defining table names, the loader imports the existing dataset configuration.

```python
from scripts.ingestion.datasets import DATASETS
```

The warehouse tables are automatically generated.

```python
TABLES = [
    dataset["table"]
    for dataset in DATASETS
]
```

This creates a single source of truth for every pipeline stage.

The same dataset configuration is now reused by:

- PostgreSQL ingestion
- Parquet export
- DuckDB warehouse loading

Future pipeline stages can reuse the same configuration without introducing duplicate code.

---

# Why Load Every Table Automatically?

Instead of writing code like:

```python
load_customers()

load_orders()

load_products()

load_reviews()
```

the warehouse loader simply loops through the dataset configuration.

```text
datasets.py

        │

        ▼

category_translation

customers

sellers

products

geolocation

orders

order_items

order_payments

order_reviews
```

Every table follows exactly the same loading process.

Advantages include:

- Less code
- Easier maintenance
- Better scalability
- Lower risk of human error

Adding a new dataset only requires updating `datasets.py`.

The warehouse loader automatically processes the new table during the next execution.

---

# Script Implementation

The entire warehouse creation process is implemented inside:

```text
scripts/

└── warehouse/

    └── load_duckdb.py
```

Instead of placing all logic inside one large function, the script is divided into several reusable functions.

This improves:

- Readability
- Maintainability
- Scalability
- Debugging
- Reusability

The overall execution flow is shown below.

```text
main()

│

├── create_warehouse_directory()

├── get_connection()

├── load_parquet()

├── count_rows()

├── generate_report()

└── print_summary()
```

Each function performs a single responsibility.

---

# Project Configuration

At the beginning of the script, several project paths are defined.

```python
BASE_DIR

PARQUET_DIR

WAREHOUSE_DIR

DOCS_DIR

DATABASE_FILE

REPORT_FILE
```

These variables centralize all important project locations.

Instead of hardcoding file paths throughout the script, every directory is managed from one location.

This improves maintainability and makes the project easier to move between different environments.

---

# create_warehouse_directory()

Purpose

Create the warehouse directory if it does not already exist.

Workflow

```text
Check Directory

↓

Create Directory

↓

Continue
```

The function uses:

```python
WAREHOUSE_DIR.mkdir(
    parents=True,
    exist_ok=True
)
```

Advantages

- Prevents file write errors
- Automatically prepares the warehouse folder
- Safe to execute multiple times

---

# get_connection()

Purpose

Create a connection to the DuckDB database.

Workflow

```text
Create Warehouse Directory

↓

Connect to DuckDB

↓

Return Connection Object
```

The function uses:

```python
duckdb.connect(
    DATABASE_FILE
)
```

Unlike PostgreSQL, DuckDB automatically creates the database file if it does not already exist.

No manual database creation is required.

---

# load_parquet()

Purpose

Load a Parquet file into DuckDB.

Workflow

```text
Locate Parquet File

↓

Read Parquet

↓

Create DuckDB Table

↓

Load Data
```

The function executes:

```sql
CREATE OR REPLACE TABLE table_name AS

SELECT *

FROM read_parquet(...)
```

DuckDB automatically:

- Reads the Parquet schema
- Creates the table
- Detects data types
- Loads every record

No manual SQL table definition is required.

---

# Why Use CREATE OR REPLACE?

The loader uses:

```sql
CREATE OR REPLACE TABLE
```

instead of

```sql
CREATE TABLE
```

Advantages

- Existing tables are automatically replaced
- Re-running the pipeline does not create duplicate data
- Simplifies development
- Supports idempotent execution

This makes the warehouse loader safe to execute multiple times.

---

# count_rows()

Purpose

Validate that every table was successfully loaded.

Workflow

```text
DuckDB Table

↓

SELECT COUNT(*)

↓

Return Row Count
```

The returned row count is later included in the warehouse summary.

This provides a simple validation that every table contains the expected number of records.

---

# Warehouse Metadata

After each successful load, metadata is stored.

Each table records:

- Table name
- Row count

Example

```text
customers

Rows:
99,441
```

The total number of rows is also accumulated.

```text
TOTAL_ROWS
```

This information is later used to generate the warehouse report.

---

# generate_report()

Purpose

Automatically generate a Markdown report summarizing the warehouse loading process.

The report contains:

- Execution timestamp
- Number of tables loaded
- Total rows
- Row count for every table
- Database filename

Output location

```text
docs/

└── duckdb_load_report.md
```

Instead of manually documenting every execution, the report is generated automatically after each successful pipeline run.

This creates a reproducible execution record for future reference.

---

# main()

The `main()` function orchestrates the complete warehouse loading process.

Workflow

```text
Start Pipeline

↓

Connect to DuckDB

↓

Loop Through Every Table

↓

Load Parquet File

↓

Count Rows

↓

Store Metadata

↓

Close Connection

↓

Generate Report

↓

Print Warehouse Summary
```

The loader automatically processes every dataset defined inside `datasets.py`.

Adding a new dataset requires updating only the shared dataset configuration.

The warehouse loader automatically includes the new table during the next execution.

This design minimizes duplicate code and keeps the pipeline scalable.

---

# Warehouse Validation

After the warehouse loading process completed, several validation checks were performed.

Validation Checklist

✅ DuckDB database created successfully

✅ All 9 Parquet files loaded

✅ All expected warehouse tables created

✅ Row counts successfully validated

✅ Warehouse report generated

✅ No failed tables

These validation checks confirm that the analytical warehouse was built successfully.

---

# Warehouse Report

Every successful execution automatically generates a Markdown report.

Output location

```text
docs/

└── duckdb_load_report.md
```

The report contains:

- Execution timestamp
- Number of tables loaded
- Total rows loaded
- Row count for every table
- Database filename

Example

```text
# DuckDB Warehouse Report

Generated:
2026-07-12

Tables Loaded:
9

Total Rows:
1,551,698
```

This provides an execution log that can be reviewed after every warehouse refresh.

---

# Warehouse Verification

After loading the warehouse, several SQL queries were executed to verify the results.

List all warehouse tables

```sql
SHOW TABLES;
```

Result

```text
category_translation
customers
geolocation
order_items
order_payments
order_reviews
orders
products
sellers
```

Verify row count

```sql
SELECT COUNT(*)

FROM customers;
```

Result

```text
99,441
```

These verification queries confirmed that the warehouse was successfully populated.

---

# Challenges Encountered

Several implementation issues were encountered during this phase.

## 1. Python Module Execution

Initially the warehouse loader produced no output.

Cause

The following block was accidentally indented inside the `main()` function.

```python
if __name__ == "__main__":
    main()
```

Because of the incorrect indentation, `main()` was never executed.

Solution

The block was moved outside the function.

This restored normal execution.

---

## 2. Duplicate Success Messages

Initially each table printed two success messages.

Example

```text
SUCCESS - customers

SUCCESS - 99,441 rows
```

Cause

Both `load_parquet()` and `main()` printed successful execution messages.

Solution

The duplicate message inside `load_parquet()` was removed.

The final output became cleaner.

---

## 3. Markdown Report Formatting

A small formatting issue appeared at the end of the generated Markdown report.

Cause

The report did not end with a trailing newline.

Solution

A blank line was appended before writing the report file.

The report now renders cleanly in Markdown viewers and GitHub.

---

# Lessons Learned

This phase introduced several important data engineering concepts.

Topics learned

- Data Warehouse architecture
- DuckDB
- Embedded analytical databases
- Apache Parquet integration
- Warehouse validation
- Automated reporting
- SQL verification
- Reusable pipeline design
- Metadata collection

These concepts are widely used in modern analytics engineering.

---

# Phase Summary

Phase 4 successfully transformed the Parquet Data Lake into a fully functional analytical Data Warehouse.

The completed pipeline is shown below.

```text
Raw CSV Files
      │
      ▼
PostgreSQL Operational Database
      │
      ▼
Apache Parquet Data Lake
      │
      ▼
DuckDB Data Warehouse
```

The warehouse now serves as the primary analytical database for the remainder of the project.

All future transformations will be executed against DuckDB rather than PostgreSQL.

In the next phase, dbt will transform the warehouse tables into staging, intermediate and mart models, creating business-ready datasets for reporting and dashboard development.

---

# Phase Completion

Phase 4 Deliverables

✅ DuckDB warehouse created

✅ 9 warehouse tables loaded

✅ Row count validation completed

✅ Warehouse report generated

✅ Warehouse successfully verified using SQL

The project now contains a complete local analytics platform consisting of:

- Operational Database
- Data Lake
- Data Warehouse

The next phase introduces dbt, where raw warehouse tables will be transformed into analytical models following modern Analytics Engineering best practices.