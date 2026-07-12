# Phase 5 - dbt Data Transformations

## Objective

The objective of this phase is to transform raw warehouse tables into clean, reusable, analytics-ready datasets using **dbt (Data Build Tool)**.

Unlike Python ETL scripts, dbt focuses purely on SQL-based transformations inside the data warehouse. It enables modular SQL development, dependency management, automated testing, documentation generation, and data lineage visualization.

After completing this phase, the project follows a modern Analytics Engineering architecture.

---

# Why dbt?

Instead of writing large SQL scripts manually, dbt allows transformations to be broken into reusable layers.

Benefits include:

- Modular SQL models
- Dependency management using `ref()`
- Source management using `source()`
- Automatic lineage graph
- Built-in testing
- Built-in documentation
- Version control friendly
- Production-ready workflow

---

# Analytics Engineering Architecture

```
Raw Tables
      │
      ▼
Sources
      │
      ▼
Staging
      │
      ▼
Intermediate
      │
      ▼
Marts
      │
      ▼
Business Dashboard
```

---

# Project Structure

```
dbt_olist/

├── analyses/
├── macros/
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── seeds/
├── snapshots/
├── tests/
├── dbt_project.yml
└── profiles.yml
```

---

# Configuration Files

## profiles.yml

The `profiles.yml` file defines the database connection used by dbt.

For this project, dbt connects directly to the local DuckDB warehouse.

Database:

```
warehouse/olist.duckdb
```

---

## dbt_project.yml

The `dbt_project.yml` file defines the project configuration.

It specifies:

- Project name
- Model locations
- Materialization strategy
- Target schema

This file acts as the central configuration for the dbt project.

---

# Source Layer

The Source layer represents the raw tables loaded into DuckDB.

Nine source tables were configured.

Sources:

- customers
- orders
- products
- sellers
- geolocation
- order_items
- order_payments
- order_reviews
- category_translation

The `source()` function is used so downstream models always reference a single source definition instead of hardcoding table names.

Example:

```sql
SELECT *

FROM {{ source('raw', 'customers') }}
```

This improves maintainability and ensures all downstream models inherit the same source configuration.

# Staging Layer

The Staging layer is the first transformation layer built on top of the raw source tables.

Its primary purpose is to standardize the raw datasets without applying business logic.

Responsibilities include:

- Renaming columns if necessary
- Standardizing naming conventions
- Selecting required columns
- Removing unnecessary fields
- Creating a clean foundation for downstream models

Nine staging models were created.

Models:

- stg_customers
- stg_orders
- stg_products
- stg_sellers
- stg_geolocation
- stg_order_items
- stg_order_payments
- stg_order_reviews
- stg_category_translation

Each staging model references its corresponding source using the `source()` function.

Example:

```sql
SELECT *

FROM {{ source('raw', 'customers') }}
```

No business calculations are performed in the staging layer.

---

# Intermediate Layer

The Intermediate layer combines multiple staging models into reusable business entities.

Instead of every dashboard joining multiple tables repeatedly, the joins are performed once inside dbt.

This layer improves maintainability and encourages SQL reuse.

Seven intermediate models were created.

Models:

- int_customer_orders
- int_orders
- int_order_items
- int_payment_summary
- int_delivery_metrics
- int_product_sales
- int_review_metrics

Examples of transformations performed:

- Customer and Order joins
- Payment aggregation
- Product sales aggregation
- Delivery metrics
- Review metrics

Unlike the staging layer, business logic is introduced here.

All intermediate models reference staging models using the `ref()` function.

Example:

```sql
SELECT *

FROM {{ ref('stg_orders') }}
```

The `ref()` function automatically creates dependencies between models and enables dbt to execute transformations in the correct order.

---

# Mart Layer

The Mart layer contains the final analytics-ready datasets.

These datasets are designed specifically for reporting and dashboarding.

The Mart layer follows a Star Schema architecture consisting of Dimension tables and Fact tables.

Dimension tables describe business entities.

Fact tables store measurable business events.

---

## Dimension Tables

Five dimension tables were created.

### dim_customer

Contains customer attributes.

Columns include:

- customer_id
- customer_unique_id
- customer_city
- customer_state

---

### dim_product

Contains product information.

Columns include:

- product_id
- category
- dimensions
- weight
- photos

---

### dim_seller

Contains seller information.

Columns include:

- seller_id
- seller_city
- seller_state

---

### dim_geolocation

Contains geolocation reference data.

---

### dim_date

Contains calendar dates derived from order purchase timestamps.

---

## Fact Tables

Four fact tables were created.

### fact_orders

Stores one record per order.

Includes:

- order_id
- customer_id
- order_status
- purchase timestamp
- delivery dates

---

### fact_order_items

Stores purchased products for each order.

---

### fact_payments

Stores payment information aggregated by order.

---

### fact_reviews

Stores customer review information.

---

# Executive Dashboard Model

A final business model named `executive_dashboard` was created.

This model aggregates key business metrics into a single dataset for dashboard consumption.

Current KPIs include:

- Total Orders
- Total Customers
- Total Revenue
- Average Order Value

This model serves as the primary data source for the executive dashboard that will be built during the Analytics phase.

---

# dbt Dependency Graph

The completed transformation pipeline follows this dependency flow.

```
Sources

↓

Staging

↓

Intermediate

↓

Marts

↓

Executive Dashboard
```

The dependency graph is automatically managed by dbt through the use of `source()` and `ref()`.

# schema.yml

dbt uses `schema.yml` files to define metadata, documentation, and automated tests for each model.

Three schema files were created.

```
models/

staging/schema.yml

intermediate/schema.yml

marts/schema.yml
```

Each schema file documents the purpose of every model and defines column-level data quality rules.

Example:

```yaml
models:

  - name: dim_customer

    columns:

      - name: customer_id

        tests:

          - unique

          - not_null
```

---

# Data Quality Tests

One of dbt's major advantages is built-in automated testing.

Instead of manually writing SQL validation queries, tests are defined declaratively inside `schema.yml`.

Three types of tests were implemented.

## Unique Tests

Ensures that primary keys do not contain duplicate values.

Examples:

- customer_id
- product_id
- seller_id
- order_id

Example:

```yaml
tests:

- unique
```

---

## Not Null Tests

Ensures required columns never contain NULL values.

Example:

```yaml
tests:

- not_null
```

---

## Relationship Tests

Relationship tests verify referential integrity between fact tables and dimension tables.

Example:

```
fact_orders.customer_id

↓

dim_customer.customer_id
```

This ensures that every customer referenced by the fact table actually exists inside the customer dimension.

Example:

```yaml
tests:

- relationships:

    arguments:

      to: ref('dim_customer')

      field: customer_id
```

---

# Test Execution

After all models and schema files were completed, dbt tests were executed.

Command:

```bash
dbt test
```

Results:

```
PASS = 32

WARN = 0

ERROR = 0
```

This confirms:

- No duplicate primary keys
- No NULL values in required columns
- Valid foreign-key relationships
- Successful warehouse validation

---

# dbt Documentation

dbt automatically generates project documentation.

Documentation includes:

- Model descriptions
- Column descriptions
- Tests
- Sources
- Data lineage
- SQL dependencies

Documentation was generated using:

```bash
dbt docs generate
```

Generated files include:

- manifest.json
- catalog.json
- index.html
- run_results.json

These files can be used to serve an interactive documentation website.

---

# Data Lineage

dbt automatically builds a dependency graph using `source()` and `ref()`.

The completed lineage for this project is:

```
Raw Sources

↓

Staging Models

↓

Intermediate Models

↓

Dimension Tables

↓

Fact Tables

↓

Executive Dashboard
```

This lineage ensures every model is executed in the correct order without manual dependency management.

---

# dbt Commands Used

Project Validation

```bash
dbt debug
```

List Models

```bash
dbt ls
```

List Sources

```bash
dbt ls --resource-type source
```

Run Staging Models

```bash
dbt run --select staging
```

Run Intermediate Models

```bash
dbt run --select intermediate
```

Run Mart Models

```bash
dbt run --select marts
```

Run Tests

```bash
dbt test
```

Generate Documentation

```bash
dbt docs generate
```

Serve Documentation

```bash
dbt docs serve
```

# Lessons Learned

During this phase, several important Analytics Engineering concepts were learned.

## Modern Layered Architecture

Instead of writing one large SQL query, transformations were separated into logical layers.

```
Raw Tables

↓

Sources

↓

Staging

↓

Intermediate

↓

Marts

↓

Dashboard
```

This architecture improves maintainability, readability, and scalability.

---

## Source vs Ref

Two important dbt functions were introduced.

### source()

Used for referencing raw tables.

Example:

```sql
{{ source('raw', 'customers') }}
```

### ref()

Used for referencing another dbt model.

Example:

```sql
{{ ref('stg_customers') }}
```

The `ref()` function automatically creates dependencies between models and ensures they are executed in the correct order.

---

## Analytics Engineering Workflow

The complete Analytics Engineering workflow now consists of:

```
DuckDB

↓

dbt Sources

↓

Staging Models

↓

Intermediate Models

↓

Mart Models

↓

Business Dashboard
```

This architecture is widely adopted by modern data teams.

---

# Deliverables

The following deliverables were completed during Phase 5.

## Configuration

- dbt Project
- profiles.yml
- dbt_project.yml

## Sources

- 9 source definitions

## Models

- 9 Staging Models
- 7 Intermediate Models
- 5 Dimension Tables
- 4 Fact Tables
- 1 Executive Dashboard Model

Total Models Created:

```
26
```

---

## Testing

Completed:

- Unique Tests
- Not Null Tests
- Relationship Tests

Results:

```
32 Tests Passed
0 Failed
```

---

## Documentation

Completed:

- schema.yml
- dbt Documentation
- Data Lineage
- Catalog Generation

---

# Phase Outcome

The DuckDB warehouse has successfully been transformed into an analytics-ready warehouse using dbt.

The warehouse now follows a modern layered architecture consisting of Sources, Staging, Intermediate, and Mart models.

Automated data quality tests ensure data integrity before downstream reporting.

Documentation and lineage generation provide transparency and improve maintainability.

This phase establishes the Analytics Engineering layer of the project and prepares the warehouse for orchestration using Apache Airflow in the next phase.

---

# Next Phase

Phase 6

Apache Airflow Orchestration

Objectives:

- Automate the entire pipeline using DAGs.
- Execute all ETL stages in sequence.
- Run dbt transformations automatically.
- Execute dbt tests after transformations.
- Generate documentation after successful execution.
- Prepare the pipeline for scheduling and production deployment.