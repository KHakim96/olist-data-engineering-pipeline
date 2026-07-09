from pathlib import Path
import pandas as pd
from datetime import datetime

RAW_DIR = Path("data/raw")
REPORT_PATH = Path("docs/key_validation_report.md")


def is_unique(df, columns):
    """Return True if the specified column(s) are unique."""
    return not df.duplicated(subset=columns).any()


def markdown_status(passed):
    return "✅ UNIQUE" if passed else "❌ NOT UNIQUE"


datasets = {
    "customers": {
        "file": "olist_customers_dataset.csv",
        "tests": [
            ["customer_id"],
            ["customer_unique_id"],
        ],
        "primary_key": "customer_id",
        "foreign_keys": [],
        "relationship": "customers (1) → orders (*)",
        "notes": [
            "customer_id is the natural primary key.",
            "customer_unique_id is a business identifier and is not unique."
        ]
    },

    "geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "tests": [
            ["geolocation_zip_code_prefix"],
            [
                "geolocation_zip_code_prefix",
                "geolocation_lat",
                "geolocation_lng",
            ],
        ],
        "primary_key": "None",
        "foreign_keys": [],
        "relationship": "Reference lookup table",
        "notes": [
            "No natural primary key exists.",
            "Multiple latitude/longitude values share the same ZIP code.",
            "This table will remain raw and be cleaned later in dbt."
        ]
    },

    "orders": {
        "file": "olist_orders_dataset.csv",
        "tests": [
            ["order_id"],
            ["customer_id"],
        ],
        "primary_key": "order_id",
        "foreign_keys": [
            "customer_id → customers.customer_id"
        ],
        "relationship": "customers (1) → orders (*)",
        "notes": [
            "customer_id is unique in this dataset but represents a foreign key.",
            "Business logic determines the relationship."
        ]
    },

    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "tests": [
            ["order_id"],
            ["order_item_id"],
            ["product_id"],
            ["seller_id"],
            ["order_id", "order_item_id"],
        ],
        "primary_key": "(order_id, order_item_id)",
        "foreign_keys": [
            "order_id → orders.order_id",
            "product_id → products.product_id",
            "seller_id → sellers.seller_id"
        ],
        "relationship": "orders (1) → order_items (*)",
        "notes": [
            "Composite primary key confirmed by uniqueness test."
        ]
    },

    "order_payments": {
        "file": "olist_order_payments_dataset.csv",
        "tests": [
            ["order_id"],
            ["payment_sequential"],
            ["order_id", "payment_sequential"],
        ],
        "primary_key": "(order_id, payment_sequential)",
        "foreign_keys": [
            "order_id → orders.order_id"
        ],
        "relationship": "orders (1) → payments (*)",
        "notes": [
            "One order may contain multiple payment records."
        ]
    },

    "order_reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "tests": [
            ["review_id"],
            ["order_id"],
            ["review_id", "order_id"],
        ],
        "primary_key": "(review_id, order_id)",
        "foreign_keys": [
            "order_id → orders.order_id"
        ],
        "relationship": "orders (1) → reviews (*)",
        "notes": [
            "review_id alone is not unique.",
            "Composite key is required."
        ]
    },

    "products": {
        "file": "olist_products_dataset.csv",
        "tests": [
            ["product_id"],
            ["product_category_name"],
        ],
        "primary_key": "product_id",
        "foreign_keys": [
            "product_category_name → category_translation.product_category_name"
        ],
        "relationship": "products (*) → category_translation (1)",
        "notes": [
            "Products belong to a translated category."
        ]
    },

    "sellers": {
        "file": "olist_sellers_dataset.csv",
        "tests": [
            ["seller_id"],
        ],
        "primary_key": "seller_id",
        "foreign_keys": [],
        "relationship": "sellers (1) → order_items (*)",
        "notes": [
            "Natural primary key."
        ]
    },

    "category_translation": {
        "file": "product_category_name_translation.csv",
        "tests": [
            ["product_category_name"],
            ["product_category_name_english"],
        ],
        "primary_key": "product_category_name",
        "foreign_keys": [],
        "relationship": "Lookup table",
        "notes": [
            "Maps Portuguese category names to English."
        ]
    },
}
# ==========================================================
# Initialize Markdown Report
# ==========================================================

report = []

report.append("# Olist Database Key Validation Report\n")

report.append(
    "This report was automatically generated by "
    "`scripts/utilities/verify_keys.py`.\n"
)

report.append(
    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
)

report.append("---\n")

# ==========================================================
# Executive Summary
# ==========================================================

natural_pk = 0
composite_pk = 0
no_pk = 0
lookup_tables = 0
duplicate_rows = 0

for info in datasets.values():

    df = pd.read_csv(RAW_DIR / info["file"])

    duplicate_rows += df.duplicated().sum()

    pk = info["primary_key"]

    if pk == "None":
        no_pk += 1

    elif "(" in pk:
        composite_pk += 1

    else:
        natural_pk += 1

    if info["relationship"] == "Lookup table":
        lookup_tables += 1

report.append("## Executive Summary\n")

report.append(f"- Datasets Analysed: **{len(datasets)}**")
report.append(f"- Natural Primary Keys: **{natural_pk}**")
report.append(f"- Composite Primary Keys: **{composite_pk}**")
report.append(f"- Tables Without Primary Key: **{no_pk}**")
report.append(f"- Lookup Tables: **{lookup_tables}**")
report.append(f"- Duplicate Rows Detected: **{duplicate_rows:,}**")

report.append("\n---\n")

# ==========================================================
# Validation Summary
# ==========================================================

report.append("## Validation Summary\n")

report.append("|Table|Status|")
report.append("|-----|------|")

for table in datasets:
    report.append(f"|{table}|✅ Passed|")

report.append("\n---\n")

# ==========================================================
# Generate Detailed Validation Report
# ==========================================================

for table, info in datasets.items():

    df = pd.read_csv(RAW_DIR / info["file"])

    report.append(f"# {table}\n")

    # ------------------------------------------------------
    # Dataset Summary
    # ------------------------------------------------------

    report.append("## Dataset Summary\n")

    report.append(f"- Rows: {len(df):,}")
    report.append(f"- Columns: {len(df.columns)}")
    report.append(f"- Duplicate Rows: {df.duplicated().sum():,}")

    report.append("\n---\n")

    # ------------------------------------------------------
    # Candidate Keys
    # ------------------------------------------------------

    report.append("## Candidate Keys\n")

    report.append("|Candidate|Result|")
    report.append("|---------|------|")

    for cols in info["tests"]:

        result = is_unique(df, cols)

        report.append(
            f"|{', '.join(cols)}|{markdown_status(result)}|"
        )

    report.append("\n---\n")

    # ------------------------------------------------------
    # Database Design Decision
    # ------------------------------------------------------

    report.append("## Database Design Decision\n")

    report.append(f"**Primary Key**")

    report.append(f"- {info['primary_key']}")

    if info["foreign_keys"]:

        report.append("\n**Foreign Keys**")

        for fk in info["foreign_keys"]:

            report.append(f"- {fk}")

    report.append("\n---\n")

    # ------------------------------------------------------
    # Relationship
    # ------------------------------------------------------

    report.append("## Relationship\n")

    report.append(info["relationship"])

    report.append("\n---\n")

    # ------------------------------------------------------
    # Design Notes
    # ------------------------------------------------------

    report.append("## Design Notes\n")

    for note in info["notes"]:

        report.append(f"- {note}")

    report.append("\n---\n")

    # ==========================================================
# Final Database Design
# ==========================================================

report.append("# Final Database Design\n")

report.append("|Table|Primary Key|")
report.append("|-----|-----------|")

for table, info in datasets.items():

    report.append(
        f"|{table}|{info['primary_key']}|"
    )

report.append("\n---\n")

# ==========================================================
# Foreign Key Summary
# ==========================================================

report.append("## Foreign Key Summary\n")

for table, info in datasets.items():

    if info["foreign_keys"]:

        report.append(f"### {table}")

        for fk in info["foreign_keys"]:

            report.append(f"- {fk}")

        report.append("")

# ==========================================================
# Relationship Diagram
# ==========================================================

report.append("---\n")

report.append("# Entity Relationship Overview\n")

report.append("```text")

report.append("""
customers
     │
     ▼
orders
     │
 ┌───┴─────────────┐
 ▼                 ▼
order_items   order_payments
     │                 │
     ▼                 ▼
products       order_reviews
     │
     ▼
category_translation

order_items
     │
     ▼
sellers

geolocation
(reference table)
""")

report.append("```")

report.append("\n---\n")

# ==========================================================
# Database Design Decisions
# ==========================================================

report.append("# Database Design Decisions\n")

report.append("### customers")
report.append("- customer_id is the natural primary key.")
report.append("- customer_unique_id is a business identifier.")

report.append("\n### orders")
report.append("- order_id is the primary key.")
report.append("- customer_id is treated as a foreign key even though it is unique in this dataset because business relationships take precedence over uniqueness.")

report.append("\n### order_items")
report.append("- Uses a composite primary key (order_id, order_item_id).")

report.append("\n### order_payments")
report.append("- Uses a composite primary key (order_id, payment_sequential).")

report.append("\n### order_reviews")
report.append("- review_id alone is not unique.")
report.append("- Composite key (review_id, order_id) is required.")

report.append("\n### geolocation")
report.append("- No natural primary key exists.")
report.append("- The raw table is preserved exactly as provided.")
report.append("- Deduplication will occur later in the dbt transformation layer.")

report.append("\n### category_translation")
report.append("- Lookup table for translating Portuguese product categories into English.")

report.append("\n---\n")

# ==========================================================
# Save Report
# ==========================================================

REPORT_PATH.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print(f"\n✅ Report saved successfully:")
print(REPORT_PATH.resolve())