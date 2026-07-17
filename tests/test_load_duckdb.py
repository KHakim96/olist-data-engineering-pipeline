from pathlib import Path

import duckdb

# ==========================================================
# DUCKDB DATABASE
# ==========================================================

DB_PATH = Path("warehouse/olist.duckdb")

conn = duckdb.connect(DB_PATH)

# ==========================================================
# TEST DATABASE EXISTS
# ==========================================================


def test_duckdb_exists():

    assert DB_PATH.exists()


# ==========================================================
# TEST REQUIRED TABLES EXIST
# ==========================================================


def test_required_tables_exist():

    required_tables = [
        "fact_orders",
        "fact_order_items",
        "fact_payments",
        "fact_reviews",
        "dim_customer",
        "dim_product",
        "dim_seller",
        "dim_geolocation",
        "executive_dashboard",
    ]

    existing_tables = conn.execute("""
        SHOW TABLES
    """).fetchall()

    existing_tables = [table[0] for table in existing_tables]

    for table in required_tables:

        assert table in existing_tables


# ==========================================================
# TEST FACT TABLES ARE NOT EMPTY
# ==========================================================


def test_fact_tables_not_empty():

    fact_tables = [
        "fact_orders",
        "fact_order_items",
        "fact_payments",
        "fact_reviews",
    ]

    for table in fact_tables:

        count = conn.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            """).fetchone()[0]

        assert count > 0


# ==========================================================
# TEST DIMENSION TABLES ARE NOT EMPTY
# ==========================================================


def test_dimension_tables_not_empty():

    dimension_tables = [
        "dim_customer",
        "dim_product",
        "dim_seller",
        "dim_geolocation",
    ]

    for table in dimension_tables:

        count = conn.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            """).fetchone()[0]

        assert count > 0


# ==========================================================
# TEST EXECUTIVE DASHBOARD EXISTS
# ==========================================================


def test_executive_dashboard_exists():

    count = conn.execute("""
        SELECT COUNT(*)
        FROM executive_dashboard
    """).fetchone()[0]

    assert count == 1


# ==========================================================
# TEST REVENUE IS POSITIVE
# ==========================================================


def test_total_revenue_positive():

    revenue = conn.execute("""
        SELECT total_revenue
        FROM executive_dashboard
    """).fetchone()[0]

    assert revenue > 0


# ==========================================================
# CLOSE CONNECTION
# ==========================================================


def teardown_module():

    conn.close()
