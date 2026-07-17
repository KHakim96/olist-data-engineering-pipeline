"""
Ingest raw Olist CSV datasets into PostgreSQL.
"""

from pathlib import Path
from time import perf_counter
import os

import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

from psycopg2.extras import execute_values

# from datasets import DATASETS
from scripts.ingestion.datasets import DATASETS

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Project Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = ROOT_DIR / "data" / "raw"


# ==========================================================
# PostgreSQL Configuration
# ==========================================================

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


# ==========================================================
# Runtime Statistics
# ==========================================================

START_TIME = perf_counter()

TOTAL_ROWS = 0

SUCCESSFUL_TABLES = []

FAILED_TABLES = []

# ==========================================================
# PostgreSQL Connection
# ==========================================================


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    try:

        conn = psycopg2.connect(**DB_CONFIG)

        print("Connected to PostgreSQL.")

        return conn

    except Exception as e:

        print(f"\nFailed to connect to PostgreSQL.\n")
        print(e)

        raise


# ==========================================================
# Load CSV File
# ==========================================================


def load_csv(file_name):
    """
    Load a CSV file from the raw data directory.
    """

    csv_path = RAW_DATA_DIR / file_name

    df = pd.read_csv(csv_path)

    return df


# ==========================================================
# Bulk Insert Data
# ==========================================================


def insert_dataframe(conn, table_name, df):
    """
    Insert a pandas DataFrame into PostgreSQL using execute_values().
    """

    cursor = conn.cursor()

    columns = list(df.columns)

    query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
        sql.Identifier(table_name), sql.SQL(", ").join(map(sql.Identifier, columns))
    )

    # Convert all columns to Python objects first
    df = df.astype(object)

    # Replace NaN/NaT with Python None
    df = df.where(pd.notnull(df), None)

    values = list(df.itertuples(index=False, name=None))

    try:

        execute_values(cursor, query.as_string(conn), values, page_size=5000)

        conn.commit()

    # just remove below.it is just for diagnostics purpose. It will not affect the code.
    except Exception as e:

        conn.rollback()

        print("\n========== PostgreSQL Exception ==========")
        print(type(e))
        print(e)

        if hasattr(e, "diag"):
            print("\nDiagnostics:")
            print("Column Name :", getattr(e.diag, "column_name", None))
            print("Table Name  :", getattr(e.diag, "table_name", None))
            print("Datatype    :", getattr(e.diag, "datatype_name", None))
            print("Constraint  :", getattr(e.diag, "constraint_name", None))
            print("Context     :", getattr(e.diag, "context", None))
            print("Message     :", getattr(e.diag, "message_primary", None))

        raise

    finally:

        cursor.close()


# ==========================================================
# Clear Existing Tables
# ==========================================================


def truncate_tables(conn):
    """
    Remove existing data before batch ingestion.
    """

    cursor = conn.cursor()

    cursor.execute("""
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
    """)

    conn.commit()

    cursor.close()

    print("Existing data cleared.")


# ==========================================================
# Main Pipeline
# ==========================================================


def main():
    global TOTAL_ROWS

    print("\n" + "=" * 60)
    print("OLIST POSTGRESQL DATA INGESTION")
    print("=" * 60)

    conn = get_connection()

    truncate_tables(conn)

    for dataset in DATASETS:
        table = dataset["table"]
        file = dataset["file"]

        print(f"\nLoading {table}...")

        try:
            df = load_csv(file)

            insert_dataframe(conn=conn, table_name=table, df=df)

            rows = len(df)

            TOTAL_ROWS += rows
            SUCCESSFUL_TABLES.append((table, rows))
            print(f"SUCCESS - {rows:,} rows inserted.")

        except Exception as e:
            conn.rollback()
            FAILED_TABLES.append(table)
            print(f"FAILED - {table}")
            print(e)

    # After the loop finishes checking all tables, close the connection
    if conn:
        conn.close()


# ==========================================================
# Execution Summary
# ==========================================================


def print_summary():

    elapsed = perf_counter() - START_TIME

    print("\n")
    print("=" * 60)
    print("INGESTION SUMMARY")
    print("=" * 60)

    print(f"\nTables Loaded : {len(SUCCESSFUL_TABLES)}")

    for table, rows in SUCCESSFUL_TABLES:

        print(f"{table:<25}{rows:>12,} rows")

    if FAILED_TABLES:

        print("\nFailed Tables")

        for table in FAILED_TABLES:

            print(f" - {table}")

    else:

        print("\nNo failed tables.")

    print(f"\nTotal Rows Loaded : {TOTAL_ROWS:,}")

    print(f"Elapsed Time      : {elapsed:.2f} seconds")

    print("=" * 60)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()

    print_summary()
