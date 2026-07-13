# ==========================================================
# Imports
# ==========================================================

from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator

from airflow.operators.empty import EmptyOperator

# ==========================================================
# Default Arguments
# ==========================================================

default_args = {
    "owner": "Luqman",
    "depends_on_past": False,
    "retries": 2,
}

# ==========================================================
# DAG
# ==========================================================

with DAG(
    dag_id="olist_data_engineering_pipeline",
    description="End-to-end Olist Data Engineering Pipeline",
    start_date=datetime(2026, 1, 1),
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
) as dag:
    # ==========================================================
    # Start & End
    # ==========================================================

    start = EmptyOperator(task_id="start")

    end = EmptyOperator(task_id="end")

    # ==========================================================
    # Commands
    # ==========================================================

    COMMANDS = {
        "profile": "python /opt/airflow/scripts/utilities/profile_dataset.py",
        "verify": "python /opt/airflow/scripts/utilities/verify_keys.py",
        "postgres": "python /opt/airflow/scripts/ingestion/ingest_postgres.py",
        "parquet": "PYTHONPATH=/opt/airflow python /opt/airflow/scripts/export/export_parquet.py",
        "duckdb": "PYTHONPATH=/opt/airflow python /opt/airflow/scripts/warehouse/load_duckdb.py",
        "dbt_run": "cd /opt/airflow/dbt_olist && dbt run",
        "dbt_test": "cd /opt/airflow/dbt_olist && dbt test",
        "dbt_docs": "cd /opt/airflow/dbt_olist && dbt docs generate",
    }

    # ==========================================================
    # Profile Dataset
    # ==========================================================

    profile_dataset = BashOperator(
        task_id="profile_dataset",
        bash_command=COMMANDS["profile"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # Verify Keys
    # ==========================================================

    verify_keys = BashOperator(
        task_id="verify_keys",
        bash_command=COMMANDS["verify"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # Load PostgreSQL
    # ==========================================================

    load_postgresql = BashOperator(
        task_id="load_postgresql",
        bash_command=COMMANDS["postgres"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # Export Parquet
    # ==========================================================

    export_parquet = BashOperator(
        task_id="export_parquet",
        bash_command=COMMANDS["parquet"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # Load DuckDB
    # ==========================================================

    load_duckdb = BashOperator(
        task_id="load_duckdb",
        bash_command=COMMANDS["duckdb"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # dbt Run
    # ==========================================================

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=COMMANDS["dbt_run"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # dbt Test
    # ==========================================================

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=COMMANDS["dbt_test"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # dbt Docs
    # ==========================================================

    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command=COMMANDS["dbt_docs"],
        cwd="/opt/airflow",
    )

    # ==========================================================
    # Pipeline Dependencies
    # ==========================================================

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
