"""
Dataset configuration for PostgreSQL ingestion.
"""

DATASETS = [

    {
        "table": "category_translation",
        "file": "product_category_name_translation.csv",
    },

    {
        "table": "customers",
        "file": "olist_customers_dataset.csv",
    },

    {
        "table": "sellers",
        "file": "olist_sellers_dataset.csv",
    },

    {
        "table": "products",
        "file": "olist_products_dataset.csv",
    },

    {
        "table": "geolocation",
        "file": "olist_geolocation_dataset.csv",
    },

    {
        "table": "orders",
        "file": "olist_orders_dataset.csv",
    },

    {
        "table": "order_items",
        "file": "olist_order_items_dataset.csv",
    },

    {
        "table": "order_payments",
        "file": "olist_order_payments_dataset.csv",
    },

    {
        "table": "order_reviews",
        "file": "olist_order_reviews_dataset.csv",
    }

]