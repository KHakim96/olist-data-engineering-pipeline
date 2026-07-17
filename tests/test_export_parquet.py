from pathlib import Path

import pandas as pd

from scripts.ingestion.datasets import DATASETS

# ==========================================================
# PARQUET DIRECTORY
# ==========================================================

PARQUET_DIR = Path("data/processed")


# ==========================================================
# TEST PARQUET DIRECTORY EXISTS
# ==========================================================


def test_parquet_directory_exists():

    assert PARQUET_DIR.exists()


# ==========================================================
# TEST ALL PARQUET FILES EXIST
# ==========================================================


def test_all_parquet_files_exist():

    for dataset in DATASETS:

        parquet_file = dataset["table"] + ".parquet"

        assert (PARQUET_DIR / parquet_file).exists()


# ==========================================================
# TEST PARQUET FILES ARE READABLE
# ==========================================================


def test_parquet_files_are_readable():

    for dataset in DATASETS:

        parquet_file = PARQUET_DIR / (dataset["table"] + ".parquet")

        df = pd.read_parquet(parquet_file)

        assert isinstance(df, pd.DataFrame)


# ==========================================================
# TEST PARQUET FILES ARE NOT EMPTY
# ==========================================================


def test_parquet_files_not_empty():

    for dataset in DATASETS:

        parquet_file = PARQUET_DIR / (dataset["table"] + ".parquet")

        df = pd.read_parquet(parquet_file)

        assert len(df) > 0


# ==========================================================
# TEST ROW COUNTS MATCH RAW CSV
# ==========================================================


def test_row_counts_match_raw():

    raw_dir = Path("data/raw")

    for dataset in DATASETS:

        csv = raw_dir / dataset["file"]

        parquet = PARQUET_DIR / (dataset["table"] + ".parquet")

        raw_df = pd.read_csv(csv)

        parquet_df = pd.read_parquet(parquet)

        # assert len(raw_df) == len(parquet_df)

        print(
            dataset["table"],
            len(raw_df),
            len(parquet_df),
        )

        assert len(raw_df) == len(parquet_df)
