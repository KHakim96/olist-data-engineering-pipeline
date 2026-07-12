from pathlib import Path
import duckdb

from scripts.ingestion.datasets import DATASETS

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PARQUET_DIR = BASE_DIR / "data" / "processed"

WAREHOUSE_DIR = BASE_DIR / "warehouse"

DOCS_DIR = BASE_DIR / "docs"

DATABASE_FILE = WAREHOUSE_DIR / "olist.duckdb"

REPORT_FILE = DOCS_DIR / "duckdb_load_report.md"

# ==========================================================
# Create Warehouse Directory
# ==========================================================


def create_warehouse_directory():
    """
    Create warehouse directory if it does not exist.
    """

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# DuckDB Connection
# ==========================================================


def get_connection():
    """
    Connect to DuckDB database.
    """

    create_warehouse_directory()

    conn = duckdb.connect(DATABASE_FILE)

    print("Connected to DuckDB.")

    return conn


# ==========================================================
# Tables
# ==========================================================

TABLES = [dataset["table"] for dataset in DATASETS]

# ==========================================================
# Load Parquet File
# ==========================================================


def load_parquet(conn, table_name):
    """
    Load a Parquet file into DuckDB.
    """

    parquet_file = PARQUET_DIR / f"{table_name}.parquet"

    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_parquet('{parquet_file}')
    """)

    print(f"SUCCESS - {table_name}")


# ==========================================================
# Count Rows
# ==========================================================


def count_rows(conn, table_name):
    """
    Return row count for a DuckDB table.
    """

    result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()

    return result[0]


# ==========================================================
# Summary
# ==========================================================

LOADED_TABLES = []

TOTAL_ROWS = 0

# ==========================================================
# Main
# ==========================================================


def main():

    global TOTAL_ROWS

    print("\n" + "=" * 60)
    print("OLIST DUCKDB DATA WAREHOUSE")
    print("=" * 60)

    conn = get_connection()

    for table in TABLES:

        print(f"\nLoading {table}...")

        load_parquet(conn, table)

        rows = count_rows(conn, table)

        TOTAL_ROWS += rows

        LOADED_TABLES.append((table, rows))

        print(f"SUCCESS - {rows:,} rows")

    conn.close()

    print("\n")
    print("=" * 60)
    print("WAREHOUSE SUMMARY")
    print("=" * 60)

    print(f"\nTables Loaded : {len(LOADED_TABLES)}")

    for table, rows in LOADED_TABLES:

        print(f"{table:<30}{rows:>12,}")

    print(f"\nTotal Rows : {TOTAL_ROWS:,}")

    print("=" * 60)


if __name__ == "__main__":
    main()
