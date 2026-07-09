# Phase 01 — Project Setup

---

# Objective

The objective of this phase is to prepare the complete development environment before building the data pipeline.

By the end of this phase, we should have:

* Git repository initialized
* Project folder structure created
* Python dependencies defined
* Docker environment configured
* PostgreSQL container running
* Airflow container running
* Environment variables configured

No ETL or data processing is performed in this phase.

---

# Overall Architecture

```text
                    MacBook
                       │
                       ▼
                Docker Desktop
                       │
                       ▼
                Docker Compose
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
 PostgreSQL Container         Airflow Container
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
              Future Data Pipeline
```

---

# Step 1 — Create Project Structure

Project directory:

```text
olist-data-engineering-pipeline/
```

Main folders created:

```text
config/
data/
warehouse/
scripts/
sql/
dags/
dbt_olist/
dashboards/
docs/
logs/
notes/
tests/
```

Purpose of each folder:

| Folder         | Purpose                      |
| -------------- | ---------------------------- |
| config         | Configuration files          |
| data/raw       | Original Kaggle datasets     |
| data/processed | Generated Parquet files      |
| warehouse      | DuckDB database              |
| scripts        | Python ETL scripts           |
| sql            | SQL scripts                  |
| dags           | Airflow DAGs                 |
| dbt_olist      | dbt project                  |
| dashboards     | Looker Studio documentation  |
| docs           | Project documentation        |
| logs           | Runtime logs                 |
| tests          | Unit tests                   |
| notes          | Phase-by-phase documentation |

---

# Step 2 — Initialize Git Repository

Command:

```bash
git init
```

Verify:

```bash
git status
```

Expected:

```text
On branch main
No commits yet
```

Purpose:

* Version control
* Track project changes
* Push project to GitHub later

---

# Step 3 — Create .gitignore

File:

```text
.gitignore
```

Purpose:

Prevent generated files from being committed.

Ignored items include:

* Python cache
* Virtual environment
* .env
* DuckDB database
* Parquet files
* Logs
* dbt target folder
* IDE files
* macOS files

Example:

```gitignore
.env

logs/

warehouse/*.duckdb

data/processed/*.parquet

__pycache__/
```

---

# Step 4 — Create Environment Files

Files:

```text
.env
.env.example
```

Purpose:

Store configuration separately from source code.

Important variables:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

AIRFLOW_UID

AIRFLOW__CORE__EXECUTOR

AIRFLOW__DATABASE__SQL_ALCHEMY_CONN

DUCKDB_PATH

RAW_DATA_PATH

PROCESSED_DATA_PATH

LOG_LEVEL
```

Workflow:

```text
.env.example
        │
        ▼
Copy
        │
        ▼
.env
        │
        ▼
Docker + Python read configuration
```

---

# Step 5 — Create requirements.txt

Purpose:

Defines all required Python packages.

Libraries used:

```text
pandas
numpy
pyarrow
duckdb
sqlalchemy
psycopg2-binary
python-dotenv
dbt-core
dbt-duckdb
pytest
loguru
kagglehub
```

Install later using:

```bash
pip install -r requirements.txt
```

---

# Step 6 — Create Dockerfile

Purpose:

Build a custom Airflow image with the project's Python dependencies.

Dockerfile:

```dockerfile
FROM apache/airflow:2.11.2-python3.11

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
```

Build Flow:

```text
Official Airflow Image
        │
        ▼
Install Linux Packages
        │
        ▼
Copy requirements.txt
        │
        ▼
Install Python Packages
        │
        ▼
Custom Airflow Image
```

---

# Step 7 — Create docker-compose.yml

Purpose:

Run the complete infrastructure with one command.

Containers:

```text
postgres

airflow-init

airflow-webserver

airflow-scheduler
```

Volumes mounted:

```text
dags/

scripts/

sql/

dbt_olist/

data/

warehouse/

logs/

config/
```

Purpose of each service:

| Service           | Purpose                                     |
| ----------------- | ------------------------------------------- |
| postgres          | Raw landing database                        |
| airflow-init      | Initializes Airflow database and admin user |
| airflow-webserver | Airflow UI                                  |
| airflow-scheduler | Executes DAGs                               |

---

# Step 8 — Build Docker Image

Command:

```bash
docker compose build
```

First attempt:

```text
failed to connect to the docker API
```

Reason:

Docker Desktop was not running.

Resolution:

Start Docker Desktop and wait until the Docker Engine is running.

---

# Step 9 — Start Infrastructure

Command:

```bash
docker compose up -d
```

Successful output:

```text
✔ Network Created

✔ Volume Created

✔ PostgreSQL Healthy

✔ Airflow Init Exited

✔ Airflow Scheduler Started

✔ Airflow Webserver Started
```

Explanation:

* Network allows containers to communicate.
* Volume stores PostgreSQL data persistently.
* PostgreSQL became healthy.
* Airflow Init completed initialization and exited normally.
* Scheduler started successfully.
* Webserver started successfully.

---

# Step 10 — Verify Running Containers

Command:

```bash
docker ps
```

Expected containers:

```text
olist_postgres

airflow_scheduler

airflow_webserver
```

Purpose:

Confirm all required services are running.

---

# Step 11 — Remove Obsolete Compose Version

Older Compose files contained:

```yaml
version: "3.9"
```

Modern Docker Compose v2 no longer requires this line.

It was removed to eliminate the warning:

```text
the attribute "version" is obsolete
```

---

# Infrastructure Flow

```text
MacBook
    │
    ▼
Docker Desktop
    │
    ▼
Docker Compose
    │
    ├──────────────┐
    │              │
    ▼              ▼
PostgreSQL      Airflow
                    │
                    ▼
        Python ETL (Future)
```

---

# Deliverables Completed

* Project structure created
* Git initialized
* .gitignore configured
* .env created
* .env.example created
* requirements.txt completed
* Dockerfile completed
* docker-compose.yml completed
* Docker image built
* PostgreSQL running
* Airflow initialized
* Airflow Scheduler running
* Airflow Webserver running

---

# Phase Outcome

At the end of this phase, the project infrastructure is fully operational.

The environment is ready for building the data pipeline.

The next phase will create the PostgreSQL schema, download the Olist dataset, and load the raw CSV files into PostgreSQL.
