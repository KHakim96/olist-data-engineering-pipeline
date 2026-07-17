from pathlib import Path

import duckdb

# ==========================================================
# DUCKDB CONNECTION
# ==========================================================

DB_PATH = Path("warehouse/olist.duckdb")

conn = duckdb.connect(DB_PATH)

# ==========================================================
# TEST TOTAL ORDERS
# ==========================================================


def test_total_orders():

    total_orders = conn.execute("""
        SELECT COUNT(*)
        FROM fact_orders
    """).fetchone()[0]

    assert total_orders == 99441


# ==========================================================
# TEST TOTAL CUSTOMERS
# ==========================================================


def test_total_customers():

    total_customers = conn.execute("""
        SELECT COUNT(*)
        FROM dim_customer
    """).fetchone()[0]

    assert total_customers == 99441


# ==========================================================
# TEST TOTAL PRODUCTS
# ==========================================================


def test_total_products():

    total_products = conn.execute("""
        SELECT COUNT(*)
        FROM dim_product
    """).fetchone()[0]

    assert total_products == 32951


# ==========================================================
# TEST TOTAL SELLERS
# ==========================================================


def test_total_sellers():

    total_sellers = conn.execute("""
        SELECT COUNT(*)
        FROM dim_seller
    """).fetchone()[0]

    assert total_sellers == 3095


# ==========================================================
# TEST TOTAL REVENUE
# ==========================================================


def test_total_revenue():

    revenue = conn.execute("""
        SELECT SUM(total_payment)
        FROM fact_payments
    """).fetchone()[0]

    assert revenue > 0


# ==========================================================
# TEST REVIEW SCORE RANGE
# ==========================================================


def test_review_score_range():

    min_score, max_score = conn.execute("""
        SELECT
            MIN(review_score),
            MAX(review_score)
        FROM fact_reviews
    """).fetchone()

    assert min_score == 1
    assert max_score == 5


# ==========================================================
# TEST DUPLICATE ORDER IDS
# ==========================================================


def test_duplicate_orders():

    duplicates = conn.execute("""
        SELECT COUNT(*)
        FROM (

            SELECT
                order_id

            FROM fact_orders

            GROUP BY order_id

            HAVING COUNT(*) > 1

        )
    """).fetchone()[0]

    assert duplicates == 0


# ==========================================================
# TEST ORPHAN CUSTOMERS
# ==========================================================


def test_orphan_customers():

    missing = conn.execute("""
        SELECT COUNT(*)

        FROM fact_orders o

        LEFT JOIN dim_customer c

        ON o.customer_id = c.customer_id

        WHERE c.customer_id IS NULL
    """).fetchone()[0]

    assert missing == 0


# ==========================================================
# TEST NULL ORDER IDS
# ==========================================================


def test_null_order_ids():

    nulls = conn.execute("""
        SELECT COUNT(*)
        FROM fact_orders
        WHERE order_id IS NULL
    """).fetchone()[0]

    assert nulls == 0


# ==========================================================
# CLOSE CONNECTION
# ==========================================================


def teardown_module():

    conn.close()
