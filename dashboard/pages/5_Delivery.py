import streamlit as st
import plotly.express as px

from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Delivery Dashboard",
    page_icon="🚚",
    layout="wide",
)

load_css()

# ==========================================================
# HEADER
# ==========================================================

st.title("🚚 Delivery Dashboard")
st.caption("Delivery Performance Analytics")

st.divider()

### kpi

delivery = run_query("""

SELECT

    COUNT(*) AS delivered_orders,

    ROUND(
        AVG(delivery_days),
    1) AS avg_delivery_days,

    ROUND(
        AVG(shipping_days),
    1) AS avg_shipping_days,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN delivery_status='On Time'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
    1) AS on_time_rate

FROM int_delivery_metrics

""")
##kpi card

row = delivery.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        label="🚚 Delivered Orders",
        value=f"{row.delivered_orders/1000:.1f}K",
        delta="Current",
    )

with c2:

    st.metric(
        label="⏱ Avg Delivery",
        value=f"{row.avg_delivery_days:.1f} Days",
        delta="Current",
    )

with c3:

    st.metric(
        label="📦 Avg Shipping",
        value=f"{row.avg_shipping_days:.1f} Days",
        delta="Current",
    )

with c4:

    st.metric(
        label="✅ On-Time Rate",
        value=f"{row.on_time_rate:.1f}%",
        delta="Current",
    )

st.write("")

# ==========================================================
# MONTHLY DELIVERY TREND
# ==========================================================

trend = run_query("""

SELECT

    DATE_TRUNC(
        'month',
        order_purchase_timestamp
    ) AS month,

    ROUND(
        AVG(delivery_days),
    2) AS avg_delivery_days

FROM int_delivery_metrics

GROUP BY 1

ORDER BY 1

""")

trend["month"] = trend["month"].dt.strftime("%b %Y")

fig_trend = px.line(
    trend,
    x="month",
    y="avg_delivery_days",
    markers=True,
    template="plotly_dark",
)

fig_trend.update_traces(
    line=dict(
        width=4,
        color="#3B82F6",
    ),
    marker=dict(
        size=7,
    ),
)

fig_trend.update_layout(
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
    xaxis=dict(
        title="",
        tickangle=-45,
    ),
    yaxis_title="Average Delivery Days",
)

with st.container(border=True):

    st.subheader("📈 Monthly Delivery Trend")

    st.caption("Average delivery days by purchase month")

    st.plotly_chart(
        fig_trend,
        use_container_width=True,
    )

# ==========================================================
# DELIVERY STATUS
# ==========================================================

left, right = st.columns(2, gap="large")

status = run_query("""

SELECT

    delivery_status,

    COUNT(*) AS orders

FROM int_delivery_metrics

GROUP BY delivery_status

ORDER BY orders DESC

""")

fig_status = px.pie(
    status,
    names="delivery_status",
    values="orders",
    hole=0.55,
    template="plotly_dark",
)

fig_status.update_traces(
    textinfo="percent+label",
)

fig_status.update_layout(
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
)

with left:

    with st.container(border=True):

        st.subheader("🚚 Delivery Status")

        st.caption("On-Time vs Late Deliveries")

        st.plotly_chart(
            fig_status,
            use_container_width=True,
        )

delay = run_query("""

SELECT

    delay_days

FROM int_delivery_metrics

WHERE delay_days IS NOT NULL

""")

fig_delay = px.histogram(
    delay,
    x="delay_days",
    nbins=40,
    template="plotly_dark",
)

fig_delay.update_traces(
    marker_color="#F59E0B",
)

fig_delay.update_layout(
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
    xaxis_title="Delay (Days)",
    yaxis_title="Orders",
)

with right:

    with st.container(border=True):

        st.subheader("📅 Delivery Delay Distribution")

        st.caption("Distribution of delivery delays")

        st.plotly_chart(
            fig_delay,
            use_container_width=True,
        )
