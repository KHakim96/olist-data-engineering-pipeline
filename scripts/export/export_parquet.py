from pathlib import Path
from datetime import datetime

import os
import pandas as pd
import psycopg2

from scripts.ingestion.datasets import DATASETS

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"

DOCS_DIR = BASE_DIR / "docs"

REPORT_FILE = DOCS_DIR / "parquet_export_report.md"


# ==========================================================
# PostgreSQL Configuration
# ==========================================================

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB", "olist"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}

# ==========================================================
# Tables
# ==========================================================

TABLES = [dataset["table"] for dataset in DATASETS]

# ==========================================================
# PostgreSQL Connection
# ==========================================================


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    try:

        conn = psycopg2.connect(**DB_CONFIG)

        print("Connected to PostgreSQL.")

        return conn

    except Exception as e:

        print("\nFailed to connect to PostgreSQL.\n")

        raise e


# ==========================================================
# Read PostgreSQL Table
# ==========================================================


def read_table(conn, table_name):
    """
    Read an entire PostgreSQL table into a pandas DataFrame.
    """

    query = f"""
        SELECT *
        FROM {table_name}
    """

    return pd.read_sql(query, conn)


# ==========================================================
# Export DataFrame to Parquet
# ==========================================================


def export_table(df, table_name):
    """
    Export a pandas DataFrame to a Parquet file.
    """

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / f"{table_name}.parquet"

    df.to_parquet(output_file, index=False)

    return output_file


# ==========================================================
# Get File Size
# ==========================================================


def get_file_size(file_path):
    """
    Return file size in MB.
    """

    size = file_path.stat().st_size

    return round(size / (1024 * 1024), 2)


# ==========================================================
# Generate Markdown Report
# ==========================================================


def generate_report(exported_tables, total_rows):
    """
    Generate a Markdown report for the Parquet export.
    """

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    report = []

    report.append("# Parquet Export Report\n")

    report.append(
        f"**Generated:** " f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )

    report.append(f"**Tables Exported:** {len(exported_tables)}\n")

    report.append(f"**Total Rows:** {total_rows:,}\n\n")

    report.append("| Table | Rows | Columns | Size (MB) | File |")
    report.append("|------|------:|--------:|----------:|------|")

    for table in exported_tables:
        report.append(
            f"| {table['table']} | "
            f"{table['rows']:,} | "
            f"{table['columns']} | "
            f"{table['size']:.2f} | "
            f"{table['file']} |"
        )

    report.append("")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"\nReport saved to:\n{REPORT_FILE}")


# ==========================================================
# Main Pipeline
# ==========================================================


def main():

    print("\n" + "=" * 60)
    print("OLIST PARQUET EXPORT")
    print("=" * 60)

    conn = get_connection()

    exported_tables = []

    total_rows = 0

    try:

        for table in TABLES:

            print(f"\nExporting {table}...")

            df = read_table(conn, table)

            output_file = export_table(df, table)

            rows = len(df)

            columns = len(df.columns)

            file_size = get_file_size(output_file)

            exported_tables.append(
                {
                    "table": table,
                    "rows": rows,
                    "columns": columns,
                    "file": output_file.name,
                    "size": file_size,
                }
            )

            total_rows += rows

            print(
                f"SUCCESS - "
                f"{rows:,} rows | "
                f"{columns} columns | "
                f"{file_size} MB"
            )

    finally:

        generate_report(exported_tables, total_rows)
        conn.close()

        print("\nPostgreSQL connection closed.")
        print("\n" + "=" * 60)
        print("EXPORT SUMMARY")
        print("=" * 60)

        print(f"Tables Exported : {len(exported_tables)}")
        print(f"Total Rows      : {total_rows:,}")

        print("=" * 60)

    return exported_tables, total_rows


if __name__ == "__main__":

    exported_tables, total_rows = main()
