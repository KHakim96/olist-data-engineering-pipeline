# Phase 2 — PostgreSQL Database Design & Data Ingestion

---

# Objective

The objective of Phase 2 is to build the **Relational Database Layer** of the Olist Data Engineering Pipeline.

At the end of this phase:

* Docker containers are fully operational.
* PostgreSQL database is created automatically.
* All raw Olist CSV files are ingested into PostgreSQL.
* Primary Keys and Foreign Keys are implemented where appropriate.
* Bulk loading is optimized using `psycopg2.execute_values()`.
* Missing values are converted into SQL NULLs.
* Data integrity is validated after ingestion.

This PostgreSQL database serves as the **Raw Data Warehouse** before the data is exported into Parquet format and transformed using DuckDB and dbt.

---

# Phase Architecture

```
                         Docker Compose
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
        ▼                                               ▼
 Airflow Container                              PostgreSQL 16
        │                                               │
        │ Python ETL                                    │
        └──────────────────────────────► Bulk Insert ◄──┘
                                                │
                                                ▼
                                   Raw Relational Database
```

This phase only focuses on storing the raw source data into PostgreSQL.

No business transformation is performed during ingestion.

---

# Why PostgreSQL?

Although DuckDB will later become the analytical warehouse, PostgreSQL is still used because it represents a common production OLTP system.

Using PostgreSQL allows the project to demonstrate:

* Relational database design
* Schema creation
* Primary Keys
* Foreign Keys
* SQL constraints
* Bulk data ingestion
* Transaction handling
* Error handling
* Referential integrity

These are common skills expected from Data Engineers.

---

# Technology Stack

| Component        | Technology                 |
| ---------------- | -------------------------- |
| Database         | PostgreSQL 16              |
| Containerization | Docker Compose             |
| Language         | Python 3.11                |
| Database Driver  | psycopg2                   |
| Bulk Loading     | psycopg2.execute_values    |
| Data Processing  | pandas                     |
| Orchestration    | Airflow (Docker Container) |

---

# Project Directory Used During Phase 2

```
olist-data-engineering-pipeline/

│
├── sql/
│   └── create_olist_tables.sql
│
├── scripts/
│   ├── ingestion/
│   │      ingest_postgres.py
│   │      datasets.py
│   │
│   └── utilities/
│          profile_dataset.py
│          verify_keys.py
│
├── docs/
│      profiling_report.md
│      key_validation_report.md
│
├── data/
│   ├── raw/
│   └── processed/
│
└── docker-compose.yml
```

---

# Docker Containers

The following containers were created during this phase.

```
docker ps
```

Result:

```
airflow_webserver
airflow_scheduler
olist_postgres
```

Each container has a different responsibility.

## PostgreSQL

Stores the raw relational database.

Default Port

```
5432
```

Database

```
olist
```

User

```
postgres
```

Password

```
postgres
```

---

## Airflow

Used as the execution environment for all ETL scripts.

Instead of executing Python locally,

```
python scripts/ingestion/ingest_postgres.py
```

all ETL jobs are executed inside Docker.

```
docker compose exec airflow-webserver bash
```

Reason:

Inside Docker,

```
POSTGRES_HOST=postgres
```

is automatically resolved through Docker's internal network.

This is identical to how ETL jobs are executed in production.

---

# Docker Networking

The project uses Docker's internal bridge network.

```
Airflow Container
        │
        │ host = postgres
        ▼
PostgreSQL Container
```

No localhost connection is required.

This avoids environment inconsistency between local execution and production execution.

---

# Environment Variables

```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=olist
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Airflow also shares these variables using

```
env_file:
    - .env
```

inside Docker Compose.

---

# Why Run ETL Inside Docker?

Initially the ingestion script was executed locally.

```
python scripts/ingestion/ingest_postgres.py
```

This produced

```
could not translate host name "postgres"
```

because the local machine cannot resolve Docker service names.

Solution:

Execute ETL inside the Airflow container.

```
docker compose exec airflow-webserver bash

cd /opt/airflow

python scripts/ingestion/ingest_postgres.py
```

Advantages

* Same environment as production
* Same Python packages
* Same network
* No dependency mismatch
* Easier deployment
* Easier debugging

---

# PostgreSQL Database Design Philosophy

This project follows a Medallion-style architecture.

```
CSV Files

↓

PostgreSQL (Raw Layer)

↓

Parquet Files

↓

DuckDB

↓

dbt

↓

Analytics
```

Important principle:

The PostgreSQL layer stores raw source data.

Business transformations are intentionally postponed until the dbt layer.

Keeping the raw layer unchanged makes debugging easier and preserves the original source data.

---

# Data Sources

The Olist dataset contains nine CSV files.

```
category_translation
customers
geolocation
orders
order_items
order_payments
order_reviews
products
sellers
```

Total records loaded

```
1,551,698
```

---

# Phase Deliverables

At the end of Phase 2 the project contains:

✔ Dockerized PostgreSQL

✔ Automated schema creation

✔ Primary Keys

✔ Foreign Keys

✔ Bulk data ingestion

✔ Data profiling report

✔ Key validation report

✔ Error handling

✔ Transaction rollback

✔ Bulk insert optimization

✔ Successfully loaded all 9 datasets into PostgreSQL

# Database Schema Design

---

# Objective

The objective of the schema design is to convert the raw Olist CSV files into a normalized relational database while preserving the original source data.

The schema is designed to:

* maintain referential integrity
* reduce duplicate data
* simplify future SQL queries
* support downstream analytics
* provide a clean source for the Data Lake (Parquet) layer

The database follows a **normalized relational model** instead of storing one large denormalized table.

---

# Database Overview

Nine tables are created.

```text
category_translation
customers
geolocation
orders
order_items
order_payments
order_reviews
products
sellers
```

Each CSV file maps directly to one PostgreSQL table.

```text
CSV File
      │
      ▼
PostgreSQL Table
```

No transformation is performed during ingestion.

The only changes made are:

* assigning appropriate SQL datatypes
* defining Primary Keys
* defining Foreign Keys where appropriate

---

# Database Relationship

The overall relationship between tables is shown below.

```text
Customers
     │
     │ 1 : N
     ▼
Orders
     │
     ├─────────────┬──────────────┐
     │             │              │
     ▼             ▼              ▼
Order Items   Order Payments   Order Reviews
     │
     │
     ├───────────────┐
     ▼               ▼
Products         Sellers

Category Translation
        │
        │
   (Lookup Table)

Geolocation
```

The Olist dataset is highly relational, making PostgreSQL an ideal storage layer.

---

# Table Design

## 1. customers

Purpose

Stores customer demographic information.

Primary Key

```sql
customer_id
```

Columns

| Column                   | Type         |
| ------------------------ | ------------ |
| customer_id              | VARCHAR(32)  |
| customer_unique_id       | VARCHAR(32)  |
| customer_zip_code_prefix | INTEGER      |
| customer_city            | VARCHAR(100) |
| customer_state           | CHAR(2)      |

Reasoning

* customer_id uniquely identifies each customer order.
* customer_unique_id represents the actual customer identity across multiple orders.
* ZIP code stored as INTEGER because calculations are unnecessary but sorting is supported.
* State stored as CHAR(2) because Brazilian state codes always contain two characters.

---

## 2. sellers

Purpose

Stores seller information.

Primary Key

```sql
seller_id
```

Columns

| Column                 | Type         |
| ---------------------- | ------------ |
| seller_id              | VARCHAR(32)  |
| seller_zip_code_prefix | INTEGER      |
| seller_city            | VARCHAR(100) |
| seller_state           | CHAR(2)      |

Reasoning

Very similar structure to customers.

---

## 3. products

Purpose

Stores product information.

Primary Key

```sql
product_id
```

Columns

| Column                     | Type         |
| -------------------------- | ------------ |
| product_id                 | VARCHAR(32)  |
| product_category_name      | VARCHAR(100) |
| product_name_lenght        | INTEGER      |
| product_description_lenght | INTEGER      |
| product_photos_qty         | INTEGER      |
| product_weight_g           | INTEGER      |
| product_length_cm          | INTEGER      |
| product_height_cm          | INTEGER      |
| product_width_cm           | INTEGER      |

Reasoning

All measurements are stored as INTEGER because the dataset contains whole numbers.

Weight is stored in grams.

Dimensions are stored in centimeters.

---

## Why No Foreign Key?

Originally the table contained

```sql
FOREIGN KEY(product_category_name)
REFERENCES category_translation(product_category_name)
```

During testing PostgreSQL produced

```text
Key (product_category_name) = (pc_gamer)
is not present in category_translation
```

Investigation showed that the original Olist dataset contains product categories that do not exist inside the translation table.

Instead of modifying source data, the foreign key was removed.

Reason

This PostgreSQL database represents the **Raw Layer**.

Raw data should preserve the original source exactly as received.

Missing translations will be handled later inside dbt using a LEFT JOIN.

---

## 4. category_translation

Purpose

Lookup table translating Portuguese product categories into English.

Primary Key

```sql
product_category_name
```

Columns

| Column                        | Type         |
| ----------------------------- | ------------ |
| product_category_name         | VARCHAR(100) |
| product_category_name_english | VARCHAR(100) |

This table contains only 71 rows.

---

## 5. geolocation

Purpose

Stores latitude and longitude for Brazilian ZIP codes.

Columns

| Column                      | Type          |
| --------------------------- | ------------- |
| geolocation_zip_code_prefix | INTEGER       |
| geolocation_lat             | NUMERIC(10,6) |
| geolocation_lng             | NUMERIC(10,6) |
| geolocation_city            | VARCHAR(100)  |
| geolocation_state           | CHAR(2)       |

Primary Key

None.

Reason

The dataset intentionally contains multiple latitude and longitude pairs for the same ZIP code.

Therefore no unique key exists.

---

## 6. orders

Purpose

Stores customer orders.

Primary Key

```sql
order_id
```

Foreign Keys

```sql
customer_id
→ customers.customer_id
```

Reason

Every order belongs to exactly one customer.

---

Columns

| Column                        | Type        |
| ----------------------------- | ----------- |
| order_id                      | VARCHAR(32) |
| customer_id                   | VARCHAR(32) |
| order_status                  | VARCHAR(30) |
| order_purchase_timestamp      | TIMESTAMP   |
| order_approved_at             | TIMESTAMP   |
| order_delivered_carrier_date  | TIMESTAMP   |
| order_delivered_customer_date | TIMESTAMP   |
| order_estimated_delivery_date | TIMESTAMP   |

---

## 7. order_items

Purpose

Stores every product sold within an order.

Composite Primary Key

```sql
(order_id, order_item_id)
```

Reason

One order may contain multiple products.

Example

```text
Order A

Item 1
Item 2
Item 3
```

Therefore

```text
order_id
```

alone is not unique.

Foreign Keys

```text
order_id
→ orders

product_id
→ products

seller_id
→ sellers
```

---

## 8. order_payments

Purpose

Stores payment information.

Composite Primary Key

```sql
(order_id, payment_sequential)
```

Reason

One order may have multiple payment transactions.

Example

```text
Credit Card
Voucher
Gift Card
```

Foreign Key

```text
order_id
→ orders
```

---

## 9. order_reviews

Purpose

Stores customer reviews.

Composite Primary Key

```sql
(review_id, order_id)
```

Reason

The dataset allows duplicated review IDs for different orders.

A composite key guarantees uniqueness.

Foreign Key

```text
order_id
→ orders
```

---

# Primary Keys Summary

| Table                | Primary Key                    |
| -------------------- | ------------------------------ |
| customers            | customer_id                    |
| sellers              | seller_id                      |
| products             | product_id                     |
| category_translation | product_category_name          |
| orders               | order_id                       |
| order_items          | (order_id, order_item_id)      |
| order_payments       | (order_id, payment_sequential) |
| order_reviews        | (review_id, order_id)          |
| geolocation          | None                           |

---

# Foreign Keys Summary

| Child Table    | Parent Table |
| -------------- | ------------ |
| orders         | customers    |
| order_items    | orders       |
| order_items    | products     |
| order_items    | sellers      |
| order_payments | orders       |
| order_reviews  | orders       |

---

# Data Type Selection Strategy

General rules used throughout the schema.

| Data                 | PostgreSQL Type |
| -------------------- | --------------- |
| UUID-like IDs        | VARCHAR(32)     |
| State Code           | CHAR(2)         |
| City Name            | VARCHAR(100)    |
| ZIP Code             | INTEGER         |
| Integer Measurements | INTEGER         |
| Coordinates          | NUMERIC(10,6)   |
| Timestamp            | TIMESTAMP       |
| Variable Text        | VARCHAR(100)    |

The datatypes were selected based on the profiling report generated in Phase 1 rather than assigning generic TEXT to every column.

Using more appropriate datatypes reduces storage usage, improves query performance, and makes the schema easier to understand.

---

# Schema Creation

The entire database schema is created automatically using

```text
sql/create_olist_tables.sql
```

Execution

```bash
docker exec -i olist_postgres \
psql -U postgres -d olist \
< sql/create_olist_tables.sql
```

The SQL script performs the following steps:

1. Drops existing tables in dependency order.
2. Creates all nine tables.
3. Applies Primary Keys.
4. Applies Foreign Keys.
5. Verifies each table is created by executing COUNT(*) queries.

The schema can therefore be recreated repeatedly during development without requiring manual database setup.

---

# Design Decisions

Several important engineering decisions were made during schema design.

• The PostgreSQL database stores raw source data without business transformation.

• Foreign keys are used only where the source data is known to satisfy referential integrity.

• Invalid source relationships (such as missing product category translations) are handled later in dbt rather than modifying raw data.

• Composite keys are used whenever a single column cannot uniquely identify a record.

• SQL datatypes were selected using automated profiling instead of defaulting every field to TEXT.

These decisions make the schema suitable as a production-style Raw Data Layer while keeping the downstream ELT pipeline flexible.

# Python ETL Pipeline (`ingest_postgres.py`)

---

# Objective

The purpose of `ingest_postgres.py` is to automate loading all raw CSV datasets into PostgreSQL.

Instead of manually importing each CSV using SQL commands or GUI tools, the ingestion process is fully automated using Python.

Responsibilities of the script include:

* Connecting to PostgreSQL
* Reading raw CSV files
* Converting pandas data types into PostgreSQL-compatible values
* Performing high-speed bulk inserts
* Maintaining transaction integrity
* Reporting successful and failed table loads
* Producing a loading summary

This script represents the **Extract** and **Load** phases of the ETL pipeline.

---

# Pipeline Flow

The ingestion process follows the sequence below.

```text
CSV Files
      │
      ▼
Read CSV using pandas
      │
      ▼
DataFrame
      │
      ▼
Convert NaN → NULL
      │
      ▼
Bulk Insert (execute_values)
      │
      ▼
Commit Transaction
      │
      ▼
PostgreSQL
```

Every dataset passes through the same pipeline.

---

# Dataset Configuration

Instead of hardcoding every CSV import, the project stores metadata inside

```text
scripts/ingestion/datasets.py
```

Example

```python
DATASETS = [
    {
        "table": "customers",
        "file": "olist_customers_dataset.csv"
    },
    ...
]
```

Advantages

* Easier maintenance
* Less duplicate code
* Easy to add future datasets
* Cleaner project structure

The ingestion loop simply iterates over this configuration.

---

# Database Connection

Connection is established using psycopg2.

```python
conn = psycopg2.connect(**DB_CONFIG)
```

Connection parameters are loaded from the environment variables.

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

This avoids hardcoding credentials inside the source code.

---

# Reading CSV Files

Each dataset is loaded using pandas.

```python
pd.read_csv(...)
```

Pandas provides

* fast parsing
* automatic datatype inference
* missing value detection
* DataFrame manipulation

The resulting DataFrame becomes the source for PostgreSQL insertion.

---

# Why Bulk Insert?

One possible approach is

```python
for row in dataframe:
    INSERT ...
```

However, this executes one SQL statement for every row.

For the geolocation dataset alone,

```text
1,000,163
```

INSERT statements would be executed.

This is extremely slow.

---

Instead, the project uses

```python
execute_values()
```

from psycopg2.

Example

```python
execute_values(
    cursor,
    query,
    values,
    page_size=5000
)
```

Benefits

* Thousands of rows inserted per SQL statement
* Much lower network overhead
* Faster execution
* Production-ready approach

This is the recommended bulk loading technique for PostgreSQL using Python.

---

# Why `page_size=5000`?

Loading all rows in a single SQL statement would consume excessive memory.

Instead,

```text
5000 rows
```

are inserted per batch.

Example

```text
Rows

1 - 5000

↓

5001 - 10000

↓

10001 - 15000
```

Advantages

* Lower memory usage
* Faster rollback on failure
* Better scalability
* More stable for large datasets

---

# Dynamic SQL Generation

The INSERT statement is generated automatically.

Instead of writing

```sql
INSERT INTO customers (...)
```

for every table, the query is created dynamically.

Example

```python
query = sql.SQL(
    "INSERT INTO {} ({}) VALUES %s"
)
```

Column names are extracted directly from the DataFrame.

Benefits

* Works for every dataset
* Less duplicated code
* Automatically adapts if schemas change

---

# Converting NaN into SQL NULL

One of the most important implementation details involved handling missing values.

Initially,

```python
df.where(pd.notnull(df), None)
```

was used.

However,

```text
NaN
```

inside floating-point columns remained

```text
numpy.nan
```

instead of becoming

```text
None
```

This caused PostgreSQL insertion failures.

---

Correct solution

```python
df = df.astype(object)

df = df.where(
    pd.notnull(df),
    None
)
```

Why?

Changing the DataFrame to

```python
object
```

allows pandas to replace

```text
numpy.nan
```

with genuine Python

```text
None
```

PostgreSQL automatically converts

```text
None
```

into

```sql
NULL
```

This ensures nullable columns are loaded correctly.

---

# Transaction Management

Every table load is executed inside a database transaction.

If insertion succeeds

```python
conn.commit()
```

is executed.

If any error occurs

```python
conn.rollback()
```

is executed.

Benefits

* Prevents partial inserts
* Maintains database consistency
* Avoids corrupted data

Example

```text
Insert starts

↓

Error occurs

↓

Rollback

↓

Database restored
```

No incomplete table remains in PostgreSQL.

---

# Success Tracking

Two variables are maintained throughout the ingestion process.

```python
SUCCESSFUL_TABLES
```

Stores

* table name
* row count

Example

```text
customers

99,441 rows
```

---

```python
FAILED_TABLES
```

Stores

* failed table names

Example

```text
products

order_items
```

if an exception occurs.

---

# Final Summary

After every dataset has been processed, the script prints a summary.

Example

```text
Tables Loaded : 9

category_translation

customers

...

No failed tables.

Total Rows Loaded

Elapsed Time
```

This makes validation quick and provides immediate feedback after every run.

---

# Why Python Instead of COPY?

PostgreSQL provides the extremely fast

```sql
COPY
```

command.

However, this project intentionally uses Python because the goal is to demonstrate Data Engineering skills rather than only database administration.

Python provides greater flexibility for:

* data cleaning
* logging
* validation
* orchestration
* error handling
* future transformations

The same ingestion framework can later support APIs, JSON, Excel files, cloud storage, and streaming data with minimal modification.

---

# Engineering Decisions

Several important implementation decisions were made during development.

• Dataset metadata is separated from ingestion logic.

• Bulk inserts are used instead of row-by-row inserts.

• Missing values are converted to SQL NULL before insertion.

• Transactions guarantee database consistency.

• SQL statements are generated dynamically instead of being hardcoded.

• Environment variables are used instead of embedding credentials.

These decisions improve maintainability, scalability, and portability while keeping the ingestion pipeline suitable for production environments.

# Development Journey & Debugging Log

---

# Overview

Developing the PostgreSQL ingestion pipeline was not simply a matter of writing code.

Several real-world issues were encountered during development, including Docker networking, transaction handling, pandas datatype conversion, SQL syntax errors, foreign key constraints, and data quality problems.

Instead of hiding these problems, they were documented and solved systematically.

This section records the debugging process and lessons learned throughout Phase 2.

---

# Issue 1 — Docker Networking

## Problem

The ingestion script was initially executed from the local machine.

```bash id="zh4bmx"
python scripts/ingestion/ingest_postgres.py
```

The script immediately failed with

```text id="ghzjlwm"
could not translate host name "postgres"
```

---

## Root Cause

The environment variable contained

```text id="3wjlwm"
POSTGRES_HOST=postgres
```

The hostname

```text id="mlkfx0"
postgres
```

only exists inside Docker's internal network.

The host operating system has no knowledge of Docker service names.

---

## Solution

Instead of executing Python locally,

the ETL pipeline was executed inside the Airflow container.

```bash id="7jlwmx"
docker compose exec airflow-webserver bash

cd /opt/airflow

python scripts/ingestion/ingest_postgres.py
```

---

## Lesson Learned

ETL jobs should execute inside the same environment as production.

Running inside Docker guarantees

* identical networking
* identical dependencies
* identical environment variables

---

# Issue 2 — Duplicate Primary Key Errors

## Problem

Every table immediately produced

```text id="3jlwmz"
duplicate key value violates primary key
```

even though profiling confirmed there were no duplicate records.

---

## Investigation

The profiling report showed

```text id="jlwma1"
Duplicate Rows : 0
```

Key validation also confirmed

```text id="jlwma2"
customer_id

product_id

seller_id
```

were unique.

Therefore the dataset itself was correct.

---

## Root Cause

Inside

```text id="jlwma3"
insert_dataframe()
```

the bulk insert function

```python id="jlwma4"
execute_values(...)
```

was accidentally executed twice.

The same batch of rows was inserted twice before committing.

---

## Solution

Removed the duplicated

```python id="jlwma5"
execute_values(...)
```

statement.

The function now performs only one bulk insert followed by

```python id="jlwma6"
conn.commit()
```

---

## Lesson Learned

When debugging duplicate key violations,

always verify

1. source data
2. application logic
3. transaction flow

before assuming the dataset is incorrect.

---

# Issue 3 — NaN Handling

## Problem

The products table failed with

```text id="jlwma7"
integer out of range
```

This error appeared unrelated to the data because all integer values were well within PostgreSQL limits.

---

## Investigation

A problematic product row was inspected manually.

Although missing values had been converted using

```python id="jlwma8"
df.where(pd.notnull(df), None)
```

printing the DataFrame showed

```text id="jlwma9"
nan
```

instead of

```text id="jlwmb0"
None
```

The datatype remained

```text id="jlwmb1"
numpy.float64
```

---

## Root Cause

Pandas floating-point columns cannot store Python

```python id="jlwmb2"
None
```

They automatically convert it back into

```python id="jlwmb3"
numpy.nan
```

PostgreSQL interpreted these values incorrectly during insertion.

---

## Solution

Convert every column into

```python id="jlwmb4"
object
```

before replacing missing values.

```python id="jlwmb5"
df = df.astype(object)

df = df.where(
    pd.notnull(df),
    None
)
```

Now pandas stores genuine Python

```python id="jlwmb6"
None
```

which PostgreSQL converts into SQL

```sql id="jlwmb7"
NULL
```

---

## Lesson Learned

Replacing

```python id="jlwmb8"
NaN
```

with

```python id="jlwmb9"
None
```

requires object dtype.

Otherwise pandas silently converts

```python id="jlwmc0"
None
```

back into

```python id="jlwmc1"
NaN
```

---

# Issue 4 — Foreign Key Constraint Failure

## Problem

After fixing NULL handling,

PostgreSQL produced

```text id="jlwmc2"
Foreign Key Violation
```

```
product_category_name = pc_gamer
```

did not exist inside

```text id="jlwmc3"
category_translation
```

---

## Investigation

The CSV files were inspected manually.

The translation table genuinely did not contain

```text id="jlwmc4"
pc_gamer
```

The source dataset itself was inconsistent.

---

## Root Cause

The Olist dataset contains product categories that have no corresponding translation.

This is a data quality issue rather than a coding issue.

---

## Solution

The foreign key

```sql id="jlwmc5"
products

↓

category_translation
```

was removed.

Translations will instead be joined later using

```sql id="jlwmc6"
LEFT JOIN
```

inside dbt.

---

## Lesson Learned

Raw data layers should preserve source data.

Cleaning inconsistent business data belongs in downstream transformation layers.

---

# Issue 5 — SQL Syntax Error

## Problem

After removing the foreign key,

PostgreSQL reported

```text id="jlwmc7"
relation "products" does not exist
```

---

## Investigation

The schema creation script appeared to complete successfully,

yet the

```text id="jlwmc8"
products
```

table was missing.

Inspection of

```text id="jlwmc9"
create_olist_tables.sql
```

revealed

```sql id="jlwmd0"
product_width_cm INTEGER,

);
```

---

## Root Cause

A trailing comma before

```sql id="jlwmd1"
);
```

made the SQL statement invalid.

---

## Solution

Removed the extra comma.

```sql id="jlwmd2"
product_width_cm INTEGER

);
```

The schema recreated successfully.

---

## Lesson Learned

Even a single misplaced comma can prevent an entire SQL schema from being created.

Always rerun schema creation after structural changes.

---

# Issue 6 — Order Item Foreign Key Failure

## Problem

```text id="jlwmd3"
order_items
```

failed to load because

```text id="jlwmd4"
products
```

did not exist.

---

## Root Cause

This was not an independent problem.

Because

```text id="jlwmd5"
products
```

failed earlier,

its child table

```text id="jlwmd6"
order_items
```

could not satisfy the foreign key.

---

## Solution

Once the

```text id="jlwmd7"
products
```

table loaded successfully,

the

```text id="jlwmd8"
order_items
```

table also loaded successfully without modification.

---

## Final Validation

After resolving every issue,

the ingestion pipeline successfully loaded all datasets.

```text id="jlwmd9"
Tables Loaded : 9
```

```text id="jlwme0"
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

Total Rows

```text id="jlwme1"
1,551,698
```

Failed Tables

```text id="jlwme2"
None
```

---

# Key Engineering Lessons

Throughout development several important engineering principles became clear.

• Always verify the source data before changing application code.

• Run ETL pipelines inside the same environment used in production.

• Bulk insertion requires careful transaction management.

• Pandas datatype handling can affect database behavior.

• Foreign key violations are not always software bugs; they often reveal source data quality issues.

• Raw data should remain unchanged whenever possible.

• Investigating the root cause is more valuable than applying temporary fixes.

Every issue encountered during this phase improved the robustness of the ingestion pipeline and provided practical experience with real-world Data Engineering troubleshooting.

# Validation, Best Practices & Phase Summary

---

# Database Validation

After successfully completing the ingestion pipeline, every table was verified to ensure the expected number of records had been loaded.

The validation query used was:

```sql
SELECT
    (SELECT COUNT(*) FROM customers)              AS customers,
    (SELECT COUNT(*) FROM sellers)                AS sellers,
    (SELECT COUNT(*) FROM products)               AS products,
    (SELECT COUNT(*) FROM category_translation)   AS category_translation,
    (SELECT COUNT(*) FROM geolocation)            AS geolocation,
    (SELECT COUNT(*) FROM orders)                 AS orders,
    (SELECT COUNT(*) FROM order_items)            AS order_items,
    (SELECT COUNT(*) FROM order_payments)         AS order_payments,
    (SELECT COUNT(*) FROM order_reviews)          AS order_reviews;
```

Expected Result

| Table                | Expected Rows |
| -------------------- | ------------: |
| category_translation |            71 |
| customers            |        99,441 |
| sellers              |         3,095 |
| products             |        32,951 |
| geolocation          |     1,000,163 |
| orders               |        99,441 |
| order_items          |       112,650 |
| order_payments       |       103,886 |
| order_reviews        |       100,000 |

Total Records

```text
1,551,698
```

The validation confirmed that every CSV file had been loaded into PostgreSQL without data loss.

---

# Loading Performance

Final pipeline statistics

| Metric             |                     Value |
| ------------------ | ------------------------: |
| Datasets Loaded    |                         9 |
| Total Records      |                 1,551,698 |
| Failed Tables      |                         0 |
| Bulk Insert Method | psycopg2.execute_values() |
| Batch Size         |                     5,000 |
| Execution Time     |               ~15 seconds |

Considering more than 1.5 million records were loaded, the performance is acceptable for a local development environment.

---

# Final Pipeline Flow

The completed PostgreSQL ingestion pipeline is shown below.

```text
Raw CSV Files
       │
       ▼
Profile Dataset
       │
       ▼
Key Validation
       │
       ▼
Docker Compose
       │
       ▼
Airflow Container
       │
       ▼
ingest_postgres.py
       │
       ▼
Read CSV using pandas
       │
       ▼
Convert NaN → NULL
       │
       ▼
Bulk Insert (execute_values)
       │
       ▼
PostgreSQL Database
       │
       ▼
Data Validation
```

This represents the completed Extract and Load stages of the ETL pipeline.

---

# Engineering Best Practices Applied

Several software engineering principles were followed throughout the implementation.

## Configuration Separation

Database credentials are stored inside environment variables rather than being hardcoded.

Benefits

* Improved security
* Easier deployment
* Better portability
* Environment-specific configuration

---

## Modular Design

The ingestion pipeline is separated into multiple modules.

```text
datasets.py
```

Stores dataset metadata.

```text
ingest_postgres.py
```

Contains the ETL logic.

```text
create_olist_tables.sql
```

Defines the database schema.

Benefits

* Easier maintenance
* Reduced code duplication
* Better scalability

---

## Transaction Management

Every table is loaded inside a database transaction.

```python
commit()
```

on success.

```python
rollback()
```

on failure.

This guarantees database consistency.

---

## Dynamic SQL

Instead of writing an INSERT statement for every table, SQL is generated dynamically using psycopg2.sql.

Advantages

* Less repetitive code
* Easier schema maintenance
* Supports multiple datasets automatically

---

## Bulk Loading

Bulk insertion uses

```python
execute_values()
```

instead of row-by-row INSERT statements.

Benefits

* Faster loading
* Lower network overhead
* Production-ready approach

---

## Data Integrity

Primary Keys

* Prevent duplicate records.

Foreign Keys

* Preserve relationships between tables.

Constraints

* Enforce relational consistency where appropriate.

---

## Error Handling

Every insertion is wrapped inside exception handling.

If an error occurs

* rollback transaction
* report failed table
* continue processing remaining datasets

This prevents one failure from terminating the entire pipeline.

---

# Limitations

The current implementation is intended for development and demonstration purposes.

Several production enhancements could be considered.

### COPY Command

PostgreSQL's COPY command can load large datasets faster than Python.

However, execute_values() was selected to demonstrate Python-based ETL techniques.

---

### Parallel Loading

Independent tables could be loaded concurrently.

For example

```text
customers

products

sellers

category_translation

geolocation
```

could execute in parallel before loading dependent tables.

---

### Logging

Future improvements include replacing print statements with structured logging.

Possible tools

* Python logging
* Loguru
* Airflow logging

---

### Automatic Validation

Additional validation rules may include

* Row count verification
* Data completeness
* Duplicate detection
* Foreign key validation
* Data quality metrics

---

### Index Optimization

Indexes can be created after loading to improve query performance.

Examples

```sql
CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_items_product
ON order_items(product_id);
```

Indexes were intentionally omitted during bulk loading because they slow down INSERT performance.

---

### Incremental Loading

The current implementation performs a full reload.

A production pipeline would likely support

* incremental loading
* change data capture (CDC)
* upserts
* slowly changing dimensions (SCD)

These topics will become more relevant in enterprise data engineering environments.

---

# Interview Talking Points

This project demonstrates practical experience with several important Data Engineering concepts.

Topics that can be discussed during interviews include

* Relational database design
* Docker networking
* PostgreSQL schema creation
* Transaction management
* Bulk loading techniques
* Data profiling
* Primary and Foreign Keys
* Python ETL development
* Error handling
* Debugging methodology
* Data quality issues
* Environment configuration
* Modular project structure

Rather than only describing theoretical concepts, the project provides working implementations of each.

---

# Key Lessons Learned

The PostgreSQL phase provided several important technical lessons.

* Docker networking differs from local execution.
* Bulk insertion is significantly faster than row-by-row insertion.
* pandas datatype handling directly affects database behavior.
* Raw source data should generally remain unchanged.
* Data quality issues should be addressed during transformation rather than ingestion.
* Database constraints help reveal hidden problems in source datasets.
* Small SQL syntax mistakes can prevent an entire schema from being created.
* Systematic debugging is more effective than applying random fixes.

---

# Phase 2 Deliverables

At the completion of this phase, the following components were successfully implemented.

✅ Dockerized PostgreSQL database

✅ Automated schema creation

✅ Environment variable configuration

✅ Python ETL pipeline

✅ Automated bulk ingestion

✅ Primary Keys

✅ Foreign Keys

✅ Data profiling report

✅ Key validation report

✅ Transaction management

✅ Exception handling

✅ Dynamic SQL generation

✅ NaN to SQL NULL conversion

✅ Bulk insertion using execute_values()

✅ Validation queries

✅ Successfully loaded all 9 datasets

---

# Next Phase

Phase 3 introduces the Data Lake layer.

The completed PostgreSQL database will become the source for Parquet export.

Pipeline evolution

```text
CSV Files
      │
      ▼
PostgreSQL
      │
      ▼
Parquet Files
      │
      ▼
DuckDB
      │
      ▼
dbt
      │
      ▼
Analytics Mart
      │
      ▼
Looker Studio Dashboard
```

Phase 3 focuses on exporting the relational database into efficient columnar Parquet files, which will later serve as the foundation for DuckDB and dbt transformations.

---

# Phase 2 Completion Status

Status

```text
COMPLETED ✅
```

Summary

* Docker environment configured successfully.
* PostgreSQL schema created successfully.
* All nine Olist datasets loaded successfully.
* Total of **1,551,698** records ingested.
* Data integrity verified.
* ETL pipeline tested and validated.
* PostgreSQL layer ready for downstream Data Lake implementation.
