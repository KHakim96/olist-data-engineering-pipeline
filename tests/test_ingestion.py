from pathlib import Path

import pandas as pd

from scripts.ingestion.datasets import DATASETS
from scripts.ingestion.ingest_postgres import (
    RAW_DATA_DIR,
    load_csv,
)

# ==========================================================
# TEST DATASET CONFIGURATION
# ==========================================================


def test_dataset_configuration():

    assert len(DATASETS) == 9


# ==========================================================
# TEST RAW DATA DIRECTORY EXISTS
# ==========================================================


def test_raw_data_directory_exists():

    assert RAW_DATA_DIR.exists()


# ==========================================================
# TEST ALL DATA FILES EXIST
# ==========================================================


def test_all_dataset_files_exist():

    for dataset in DATASETS:

        file_path = RAW_DATA_DIR / dataset["file"]

        assert file_path.exists()


# ==========================================================
# TEST LOAD CSV RETURNS DATAFRAME
# ==========================================================


def test_load_csv_returns_dataframe():

    df = load_csv("olist_orders_dataset.csv")

    assert isinstance(df, pd.DataFrame)


# ==========================================================
# TEST DATAFRAME IS NOT EMPTY
# ==========================================================


def test_loaded_dataframe_not_empty():

    df = load_csv("olist_orders_dataset.csv")

    assert len(df) > 0


# ==========================================================
# TEST REQUIRED COLUMN EXISTS
# ==========================================================


def test_orders_contains_order_id():

    df = load_csv("olist_orders_dataset.csv")

    assert "order_id" in df.columns


# ==========================================================
# TEST CUSTOMER DATA CONTAINS CUSTOMER ID
# ==========================================================


def test_customers_contains_customer_id():

    df = load_csv("olist_customers_dataset.csv")

    assert "customer_id" in df.columns


# ==========================================================
# TEST REVIEW SCORE RANGE
# ==========================================================


def test_review_score_range():

    df = load_csv("olist_order_reviews_dataset.csv")

    assert df["review_score"].between(1, 5).all()
