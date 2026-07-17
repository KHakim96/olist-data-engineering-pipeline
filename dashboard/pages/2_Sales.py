import streamlit as st
import plotly.express as px

from utils import run_query, load_css

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="💰",
    layout="wide",
)

load_css()

st.title("💰 Sales Dashboard")
st.caption("Sales Performance Analysis")

st.divider()

sales = run_query("""

SELECT
    SUM(p.total_payment) AS revenue,

    COUNT(DISTINCT p.order_id) AS orders,

    ROUND(AVG(p.total_payment),2) AS avg_order,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN o.order_status = 'delivered'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
    1) AS delivered_rate

FROM fact_payments p

JOIN fact_orders o
ON p.order_id = o.order_id

""")

row = sales.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="💰 Revenue",
        value=f"$ {row.revenue/1_000_000:.1f}M",
        delta="Current",
    )

with c2:
    st.metric(
        label="📦 Orders",
        value=f"{row.orders/1000:.1f}K",
        delta="Current",
    )

with c3:
    st.metric(
        label="🛒 Average Order",
        value=f"$ {row.avg_order:.0f}",
        delta="Current",
    )

with c4:

    st.metric(
        label="🚚 Delivered Rate",
        value=f"{row.delivered_rate:.1f}%",
        delta="Current",
    )

monthly = run_query("""

SELECT

DATE_TRUNC('month',o.order_purchase_timestamp) AS month,

SUM(p.total_payment) AS revenue

FROM fact_orders o

JOIN fact_payments p

ON o.order_id=p.order_id

GROUP BY 1

ORDER BY 1

""")

monthly["month"] = monthly["month"].dt.strftime("%b %Y")

fig_month = px.line(
    monthly,
    x="month",
    y="revenue",
    markers=True,
    template="plotly_dark",
)

fig_month.update_traces(line=dict(width=4))

fig_month.update_layout(height=420, xaxis_title="", yaxis_title="Revenue ($)")

fig_month.update_xaxes(tickangle=-45)

st.write("")

with st.container(border=True):

    st.subheader("📈 Monthly Revenue")

    st.plotly_chart(
        fig_month,
        use_container_width=True,
    )

###############

left, right = st.columns(2, gap="large")

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

LIMIT 10

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
    height=420,
    margin=dict(l=10, r=40, t=10, b=10),
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    xaxis_title="Revenue ($)",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with left:

    with st.container(border=True):

        st.subheader("🏆 Revenue by Category")

        st.plotly_chart(
            fig_category,
            use_container_width=True,
        )

###############

payment = run_query("""

SELECT
    payment_type,
    SUM(payment_value) AS revenue
FROM stg_order_payments
GROUP BY payment_type
ORDER BY revenue DESC

""")

fig_payment = px.pie(
    payment,
    names="payment_type",
    values="revenue",
    hole=0.55,
    template="plotly_dark",
)

fig_payment.update_traces(textinfo="percent+label")

fig_payment.update_layout(
    height=430,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=10, t=10, b=10),
)

with right:

    with st.container(border=True):

        st.subheader("💳 Revenue by Payment Method")

        st.plotly_chart(
            fig_payment,
            use_container_width=True,
        )

#################

daily = run_query("""

SELECT

    CAST(o.order_purchase_timestamp AS DATE) AS day,

    SUM(p.total_payment) AS revenue

FROM fact_orders o

JOIN fact_payments p
ON o.order_id = p.order_id

GROUP BY 1

ORDER BY 1

""")

fig_daily = px.line(
    daily,
    x="day",
    y="revenue",
    template="plotly_dark",
    markers=False,
)

fig_daily.update_traces(
    line=dict(
        width=3,
        color="#60A5FA",
    )
)

fig_daily.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10,
    ),
    xaxis_title="",
    yaxis_title="Revenue ($)",
)

with st.container(border=True):

    st.subheader("📅 Daily Sales Trend")

    st.caption("Daily revenue across all orders")

    st.plotly_chart(
        fig_daily,
        use_container_width=True,
    )

####################

left, right = st.columns(2, gap="large")

state = run_query("""

SELECT

    seller_state,

    SUM(price) AS revenue

FROM fact_order_items

GROUP BY seller_state

ORDER BY revenue DESC

""")

fig_state = px.bar(
    state,
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
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis_title="",
    yaxis_title="Revenue ($)",
    yaxis=dict(tickformat=".2s"),
)

with left:

    with st.container(border=True):

        st.subheader("🌎 Revenue by State")

        st.caption("Revenue by seller state")

        st.plotly_chart(
            fig_state,
            use_container_width=True,
        )

# right

status = run_query("""

SELECT

    order_status,

    COUNT(*) AS orders

FROM fact_orders

GROUP BY order_status

ORDER BY orders DESC

""")

fig_status = px.bar(
    status,
    x="orders",
    y="order_status",
    orientation="h",
    text="orders",
    template="plotly_dark",
)

fig_status.update_traces(
    texttemplate="%{x:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#F59E0B",
)

fig_status.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=40, t=10, b=10),
    xaxis_title="Orders",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with right:

    with st.container(border=True):

        st.subheader("🚚 Orders by Status")

        st.caption("Order status distribution")

        st.plotly_chart(
            fig_status,
            use_container_width=True,
        )
