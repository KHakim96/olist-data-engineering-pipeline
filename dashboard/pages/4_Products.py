import streamlit as st
import plotly.express as px

from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Products Dashboard",
    page_icon="📦",
    layout="wide",
)

load_css()

# ==========================================================
# HEADER
# ==========================================================

st.title("📦 Products Dashboard")
st.caption("Product Performance Analytics")

st.divider()

# ==========================================================
# KPI
# ==========================================================

products = run_query("""

SELECT

    COUNT(DISTINCT product_id) AS total_products,

    ROUND(AVG(price),2) AS avg_price,

    ROUND(AVG(freight_value),2) AS avg_freight,

    COUNT(DISTINCT product_category_name) AS total_categories

FROM fact_order_items

""")

row = products.iloc[0]

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        label="📦 Products",
        value=f"{int(row.total_products):,}",
        # delta="Current",
    )

with c2:

    st.metric(
        label="💰 Avg Price",
        value=f"$ {row.avg_price:.0f}",
        # delta="Current",
    )

with c3:

    st.metric(
        label="🚚 Avg Freight",
        value=f"$ {row.avg_freight:.0f}",
        # delta="Current",
    )

with c4:

    st.metric(
        label="🏆 Categories",
        value=f"{int(row.total_categories)}",
        # delta="Current",
    )

st.write("")

# ==========================================================
# REVENUE BY CATEGORY
# ==========================================================

category = run_query("""

SELECT

    COALESCE(
        ct.product_category_name_english,
        oi.product_category_name
    ) AS category,

    SUM(oi.price) AS revenue

FROM fact_order_items oi

LEFT JOIN category_translation ct
ON oi.product_category_name = ct.product_category_name

GROUP BY 1

ORDER BY revenue DESC

LIMIT 15

""")

fig_category = px.bar(
    category,
    x="revenue",
    y="category",
    orientation="h",
    text="revenue",
    template="plotly_dark",
)

fig_category.update_traces(
    texttemplate="%{x:.2s}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#3B82F6",
)

fig_category.update_layout(
    height=520,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(
        l=10,
        r=40,
        t=10,
        b=10,
    ),
    xaxis_title="Revenue ($)",
    yaxis_title="",
    yaxis=dict(
        categoryorder="total ascending",
    ),
)
with st.container(border=True):

    st.subheader("📈 Revenue by Product Category")

    st.caption("Top 15 product categories by revenue")

    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )

# ==========================================================
# AVERAGE PRICE BY CATEGORY
# ==========================================================

left, right = st.columns(2, gap="large")

avg_price = run_query("""

SELECT

    COALESCE(
        ct.product_category_name_english,
        oi.product_category_name
    ) AS category,

    ROUND(AVG(oi.price),2) AS avg_price

FROM fact_order_items oi

LEFT JOIN category_translation ct
ON oi.product_category_name = ct.product_category_name

GROUP BY 1

ORDER BY avg_price DESC

LIMIT 10

""")
fig_price = px.bar(
    avg_price,
    x="avg_price",
    y="category",
    orientation="h",
    text="avg_price",
    template="plotly_dark",
)

fig_price.update_traces(
    texttemplate="$ %{x:.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#10B981",
)

fig_price.update_layout(
    height=430,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=50, t=10, b=10),
    xaxis_title="Average Price ($)",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with left:

    with st.container(border=True):

        st.subheader("💰 Average Price by Category")

        st.caption("Top 10 highest average product prices")

        st.plotly_chart(
            fig_price,
            use_container_width=True,
        )

avg_freight = run_query("""

SELECT

    COALESCE(
        ct.product_category_name_english,
        oi.product_category_name
    ) AS category,

    ROUND(AVG(oi.freight_value),2) AS avg_freight

FROM fact_order_items oi

LEFT JOIN category_translation ct
ON oi.product_category_name = ct.product_category_name

GROUP BY 1

ORDER BY avg_freight DESC

LIMIT 10

""")

fig_freight = px.bar(
    avg_freight,
    x="avg_freight",
    y="category",
    orientation="h",
    text="avg_freight",
    template="plotly_dark",
)

fig_freight.update_traces(
    texttemplate="$ %{x:.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#F59E0B",
)

fig_freight.update_layout(
    height=430,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=50, t=10, b=10),
    xaxis_title="Average Freight ($)",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with right:

    with st.container(border=True):

        st.subheader("🚚 Average Freight by Category")

        st.caption("Top 10 highest shipping costs")

        st.plotly_chart(
            fig_freight,
            use_container_width=True,
        )
# ==========================================================
# PRODUCT PRICE DISTRIBUTION
# ==========================================================

left, right = st.columns(2, gap="large")

price_dist = run_query("""

SELECT

    price

FROM fact_order_items

WHERE price IS NOT NULL

""")
fig_price_dist = px.histogram(
    price_dist,
    x="price",
    nbins=40,
    template="plotly_dark",
)

fig_price_dist.update_traces(
    marker_color="#3B82F6",
)

fig_price_dist.update_layout(
    height=430,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10,
    ),
    xaxis_title="Product Price ($)",
    yaxis_title="Frequency",
)
with left:

    with st.container(border=True):

        st.subheader("📊 Product Price Distribution")

        st.caption("Distribution of product prices")

        st.plotly_chart(
            fig_price_dist,
            use_container_width=True,
        )

weight = run_query("""

SELECT

    product_weight_g

FROM dim_product

WHERE product_weight_g IS NOT NULL

""")
fig_weight = px.histogram(
    weight,
    x="product_weight_g",
    nbins=40,
    template="plotly_dark",
)

fig_weight.update_traces(
    marker_color="#10B981",
)

fig_weight.update_layout(
    height=430,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10,
    ),
    xaxis_title="Weight (g)",
    yaxis_title="Frequency",
)

with right:

    with st.container(border=True):

        st.subheader("⚖ Product Weight Distribution")

        st.caption("Distribution of product weights")

        st.plotly_chart(
            fig_weight,
            use_container_width=True,
        )
