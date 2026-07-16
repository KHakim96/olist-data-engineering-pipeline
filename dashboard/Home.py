import streamlit as st
from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="OLIST Analytics",
    page_icon="🏠",
    layout="wide",
)

load_css()

# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
<style>

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
    padding-bottom:2rem;
    max-width:1600px;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# HERO
# ==========================================================

st.title("🛒 OLIST Commerce Intelligence Platform")

st.caption("Enterprise Data Engineering Portfolio Project")

st.divider()

# ==========================================================
# ABOUT
# ==========================================================

left, right = st.columns([2, 1], gap="large")

with left:

    st.subheader("📖 Project Overview")

    st.markdown("""
This project demonstrates a complete modern **Data Engineering Pipeline**
using the Brazilian Olist E-Commerce dataset.

### Technology Stack

- PostgreSQL
- Parquet Data Lake
- DuckDB Warehouse
- dbt
- Apache Airflow
- Streamlit
- Plotly

The dashboards are built directly from the curated analytics warehouse.
""")

with right:

    st.subheader("⚙ Architecture")

    st.success("PostgreSQL")

    st.success("Parquet")

    st.success("DuckDB")

    st.success("dbt")

    st.success("Airflow")

    st.success("Streamlit")

st.write("")

# ==========================================================
# DASHBOARDS
# ==========================================================

st.subheader("📊 Available Dashboards")

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:

    with st.container(border=True):

        st.markdown("### 📈 Executive")
        st.caption("Enterprise KPI overview")
        st.page_link(
            "pages/1_Executive.py",
            label="Open Dashboard →",
            icon="📈",
        )

    with st.container(border=True):

        st.markdown("### 💰 Sales")
        st.caption("Revenue & sales analytics")
        st.page_link(
            "pages/2_Sales.py",
            label="Open Dashboard →",
            icon="💰",
        )

with c2:

    with st.container(border=True):

        st.markdown("### 👥 Customers")
        st.caption("Customer behaviour insights")
        st.page_link(
            "pages/3_Customers.py",
            label="Open Dashboard →",
            icon="👥",
        )

    with st.container(border=True):

        st.markdown("### 📦 Products")
        st.caption("Product performance")
        st.page_link(
            "pages/4_Products.py",
            label="Open Dashboard →",
            icon="📦",
        )

with c3:

    with st.container(border=True):

        st.markdown("### 🚚 Delivery")
        st.caption("Logistics & shipping")
        st.page_link(
            "pages/5_Delivery.py",
            label="Open Dashboard →",
            icon="🚚",
        )

    with st.container(border=True):

        st.markdown("### ⭐ Reviews")
        st.caption("Customer satisfaction")
        st.page_link(
            "pages/6_Reviews.py",
            label="Open Dashboard →",
            icon="⭐",
        )

with c4:

    with st.container(border=True):

        st.markdown("### 🌎 Geography")
        st.caption("Regional performance")
        st.page_link(
            "pages/7_Geography.py",
            label="Open Dashboard →",
            icon="🌎",
        )

st.write("")

st.success("Explore any dashboard above or use the sidebar navigation.")
