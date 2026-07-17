import streamlit as st
import plotly.express as px

from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

load_css()

# ==========================================================
# EXECUTIVE KPI
# ==========================================================

executive = run_query("""
SELECT *
FROM executive_dashboard
""")

row = executive.iloc[0]

# ==========================================================
# REVENUE TREND
# ==========================================================

revenue = run_query("""
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    SUM(p.total_payment) AS revenue
FROM fact_orders o
JOIN fact_payments p
ON o.order_id = p.order_id
GROUP BY 1
ORDER BY 1
""")

revenue["month"] = revenue["month"].dt.strftime("%b %Y")

fig_revenue = px.line(
    revenue,
    x="month",
    y="revenue",
    template="plotly_white",
    markers=True,
)

fig_revenue.update_traces(
    line=dict(width=4),
    marker=dict(size=7),
)

fig_revenue.update_layout(
    height=420,
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis_title="",
    yaxis_title="Revenue ($)",
)

# ==========================================================
# HEADER
# ==========================================================

st.title("📊 Executive Dashboard")
st.caption("Enterprise Business Overview")

st.divider()

# ==========================================================
# KPI
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="💰 Revenue",
        value=f"$ {row.total_revenue/1_000_000:.1f}M",
        delta="Current",
    )

with c2:
    st.metric(
        label="📦 Orders",
        value=f"{row.total_orders/1000:.1f}K",
        delta="Current",
    )

with c3:
    st.metric(
        label="👥 Unique Customers",
        value=f"{row.total_customers/1000:.1f}K",
        delta="Current",
    )

with c4:
    st.metric(
        label="🛒 Avg Order",
        value=f"$ {row.average_order_value:.0f}",
        delta="Current",
    )

st.write("")

# ==========================================================
# MAIN DASHBOARD
# ==========================================================

# ----------------------------------------------------------
# ROW 1
# ----------------------------------------------------------

# Define a uniform height for both containers to guarantee perfect alignment
BOX_HEIGHT = 460

left, right = st.columns([2.8, 1.2], gap="large")

with left:

    # Apply fixed height to the left container
    with st.container(border=True, height=BOX_HEIGHT):

        st.subheader("📈 Monthly Revenue Trend")

        # We subtract ~90px from the box height to account for the subheader
        # and padding, preventing an ugly scrollbar from appearing on the chart.
        fig_revenue.update_layout(
            height=BOX_HEIGHT - 90, margin=dict(t=20, b=10, l=10, r=10)
        )

        fig_revenue.update_xaxes(tickangle=-45)

        st.plotly_chart(
            fig_revenue,
            use_container_width=True,
        )

with right:

    highlights = run_query("""
    SELECT
        (
            SELECT
                COALESCE(
                    ct.product_category_name_english,
                    oi.product_category_name
                )
            FROM fact_order_items oi
            LEFT JOIN category_translation ct
                ON oi.product_category_name = ct.product_category_name
            GROUP BY 1
            ORDER BY SUM(oi.price) DESC
            LIMIT 1
        ) AS top_category,

        (
            SELECT seller_state
            FROM fact_order_items
            GROUP BY seller_state
            ORDER BY SUM(price) DESC
            LIMIT 1
        ) AS top_state,

        (
            SELECT ROUND(AVG(review_score),2)
            FROM fact_reviews
        ) AS avg_rating,

        (
            SELECT ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN order_status='delivered'
                        THEN 1
                        ELSE 0
                    END
                ) / COUNT(*),
            1)
            FROM fact_orders
        ) AS delivered_pct
    """)

    h = highlights.iloc[0]

    # Apply the exact same fixed height to the right container
    with st.container(border=True, height=BOX_HEIGHT):

        st.subheader("📌 Business Highlights")

        st.write("")

        st.markdown("**🏆 Top Category**")
        st.markdown(f"#### {h.top_category.replace('_',' ').title()}")
        st.write("")

        st.markdown("**🌎 Top State**")
        st.markdown(f"#### {h.top_state}")
        st.write("")

        st.markdown("**⭐ Average Rating**")
        st.markdown(f"#### {h.avg_rating:.2f} ★")
        st.write("")

        st.markdown("**📦 Delivered Orders**")
        st.markdown(f"#### {h.delivered_pct:.1f}%")

# ----------------------------------------------------------
# ROW 2
# ----------------------------------------------------------

top_categories = run_query("""

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

LIMIT 10

""")

fig_category = px.bar(
    top_categories,
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
    margin=dict(l=10, r=40, t=10, b=10),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    xaxis_title="Revenue ($)",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with st.container(border=True):

    st.subheader("🏆 Top Product Categories")

    st.caption("Top 10 categories by revenue")

    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )

st.write("")
st.write("")

# ----------------------------------------------------------
# ROW 3
# ----------------------------------------------------------

state_revenue = run_query("""

SELECT

    seller_state,

    SUM(price) AS revenue

FROM fact_order_items

GROUP BY seller_state

ORDER BY revenue DESC

LIMIT 10

""")

fig_state = px.bar(
    state_revenue,
    x="seller_state",
    y="revenue",
    text="revenue",
    template="plotly_dark",
)

fig_state.update_traces(
    texttemplate="%{y:.2s}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#10B981",
)

fig_state.update_layout(
    height=520,
    margin=dict(l=10, r=20, t=10, b=10),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    xaxis_title="",
    yaxis_title="Revenue",
    yaxis=dict(tickformat=".2s"),
)

with st.container(border=True):

    st.subheader("🌎 Revenue by State")

    st.caption("Top 10 states by revenue")

    st.plotly_chart(
        fig_state,
        use_container_width=True,
    )
