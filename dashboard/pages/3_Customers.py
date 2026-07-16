import streamlit as st
import plotly.express as px

from utils import run_query, load_css

st.set_page_config(
    page_title="Customers Dashboard",
    page_icon="👥",
    layout="wide",
)

load_css()

st.title("👥 Customers Dashboard")
st.caption("Customer Analytics")

st.divider()

customer = run_query("""

SELECT

    COUNT(DISTINCT customer_unique_id) AS customers,

    ROUND(
        COUNT(o.order_id) * 1.0 /
        COUNT(DISTINCT c.customer_unique_id),
    2) AS avg_orders,

    COUNT(DISTINCT customer_state) AS states,

    (
        SELECT
            ROUND(AVG(review_score),2)
        FROM fact_reviews
    ) AS avg_rating

FROM dim_customer c

LEFT JOIN fact_orders o
ON c.customer_id = o.customer_id

""")

## kpi card

row = customer.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="👥 Customers",
        value=f"{row.customers/1000:.1f}K",
        delta="Current",
    )

with c2:
    st.metric(
        label="🛒 Avg Orders",
        value=f"{row.avg_orders:.2f}",
        delta="Current",
    )

with c3:
    st.metric(
        label="🌎 States",
        value=f"{int(row.states)}",
        delta="Current",
    )

with c4:
    st.metric(
        label="⭐ Avg Rating",
        value=f"{row.avg_rating:.2f}",
        delta="Current",
    )

###Customer Growth

growth = run_query("""

SELECT

    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp
    ) AS month,

    COUNT(
        DISTINCT c.customer_unique_id
    ) AS customers

FROM fact_orders o

JOIN dim_customer c
ON o.customer_id = c.customer_id

GROUP BY 1

ORDER BY 1

""")

growth["month"] = growth["month"].dt.strftime("%b %Y")

fig_growth = px.line(
    growth,
    x="month",
    y="customers",
    markers=True,
    template="plotly_dark",
)

fig_growth.update_traces(
    line=dict(
        width=4,
        color="#3B82F6",
    ),
    marker=dict(
        size=7,
    ),
)

fig_growth.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(
        color="white",
    ),
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10,
    ),
    xaxis_title="",
    yaxis_title="Customers",
)

fig_growth.update_xaxes(tickangle=-45)

with st.container(border=True):

    st.subheader("📈 Customer Growth Over Time")

    st.caption("Monthly unique purchasing customers")

    st.plotly_chart(
        fig_growth,
        use_container_width=True,
    )

### Customers by State left

left, right = st.columns(2, gap="large")

state = run_query("""

SELECT

    customer_state,

    COUNT(DISTINCT customer_unique_id) AS customers

FROM dim_customer

GROUP BY customer_state

ORDER BY customers DESC

""")

fig_state = px.bar(
    state,
    x="customer_state",
    y="customers",
    text="customers",
    template="plotly_dark",
)

fig_state.update_traces(
    texttemplate="%{y:,.0f}",
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
    yaxis_title="Customers",
)

with left:

    with st.container(border=True):

        st.subheader("🌎 Customers by State")

        st.caption("Unique customers by state")

        st.plotly_chart(
            fig_state,
            use_container_width=True,
        )

## Top Customer Cities rigth

city = run_query("""

SELECT

    customer_city,

    COUNT(DISTINCT customer_unique_id) AS customers

FROM dim_customer

GROUP BY customer_city

ORDER BY customers DESC

LIMIT 10

""")

fig_city = px.bar(
    city,
    x="customers",
    y="customer_city",
    orientation="h",
    text="customers",
    template="plotly_dark",
)

fig_city.update_traces(
    texttemplate="%{x:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#3B82F6",
)

fig_city.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=40, t=10, b=10),
    xaxis_title="Customers",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with right:

    with st.container(border=True):

        st.subheader("🏙 Top Customer Cities")

        st.caption("Top 10 cities by unique customers")

        st.plotly_chart(
            fig_city,
            use_container_width=True,
        )
