import streamlit as st
import plotly.express as px

from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Reviews Dashboard",
    page_icon="⭐",
    layout="wide",
)

load_css()

# ==========================================================
# HEADER
# ==========================================================

st.title("⭐ Reviews Dashboard")
st.caption("Customer Satisfaction Analytics")

st.divider()

reviews = run_query("""

SELECT

    COUNT(*) AS total_reviews,

    ROUND(AVG(review_score),2) AS avg_rating,

    SUM(
        CASE
            WHEN review_score=5
            THEN 1
            ELSE 0
        END
    ) AS five_star,

    SUM(
        CASE
            WHEN review_score=1
            THEN 1
            ELSE 0
        END
    ) AS one_star

FROM fact_reviews

""")

row = reviews.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        label="📝 Reviews",
        value=f"{row.total_reviews/1000:.1f}K",
        delta="Current",
    )

with c2:

    st.metric(
        label="⭐ Avg Rating",
        value=f"{row.avg_rating:.2f}",
        delta="Current",
    )

with c3:

    st.metric(
        label="😊 5-Star Reviews",
        value=f"{row.five_star/1000:.1f}K",
        delta="Current",
    )

with c4:

    st.metric(
        label="😞 1-Star Reviews",
        value=f"{row.one_star/1000:.1f}K",
        delta="Current",
    )

st.write("")

## rating distribution

rating = run_query("""

SELECT

    review_score,

    COUNT(*) AS reviews

FROM fact_reviews

GROUP BY review_score

ORDER BY review_score

""")

fig_rating = px.bar(
    rating,
    x="review_score",
    y="reviews",
    text="reviews",
    template="plotly_dark",
)

fig_rating.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#F59E0B",
)

fig_rating.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis_title="Rating",
    yaxis_title="Reviews",
)

with st.container(border=True):

    st.subheader("⭐ Rating Distribution")

    st.caption("Distribution of customer review scores")

    st.plotly_chart(
        fig_rating,
        use_container_width=True,
    )

# ==========================================================
# MONTHLY REVIEW TREND
# ==========================================================

trend = run_query("""

SELECT

    DATE_TRUNC(
        'month',
        review_creation_date
    ) AS month,

    ROUND(
        AVG(review_score),
    2) AS avg_rating

FROM fact_reviews

GROUP BY 1

ORDER BY 1

""")

trend["month"] = trend["month"].dt.strftime("%b %Y")

fig_trend = px.line(
    trend,
    x="month",
    y="avg_rating",
    markers=True,
    template="plotly_dark",
)

fig_trend.update_traces(
    line=dict(width=4),
    marker=dict(size=7),
)

fig_trend.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(
        title="",
        tickangle=-45,
    ),
    yaxis_title="Average Rating",
)

with st.container(border=True):

    st.subheader("📈 Monthly Review Trend")

    st.caption("Average customer rating by month")

    st.plotly_chart(
        fig_trend,
        use_container_width=True,
    )

# 🚚 Delivery Days vs Rating      🌎 Average Rating by State

left, right = st.columns(2, gap="large")

delivery = run_query("""

SELECT

    r.review_score,

    ROUND(
        AVG(d.delivery_days),
    2) AS avg_delivery_days

FROM fact_reviews r

JOIN int_delivery_metrics d

ON r.order_id = d.order_id

GROUP BY r.review_score

ORDER BY r.review_score

""")

fig_delivery = px.bar(
    delivery,
    x="review_score",
    y="avg_delivery_days",
    text="avg_delivery_days",
    template="plotly_dark",
)

fig_delivery.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#3B82F6",
)

fig_delivery.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis_title="Review Score",
    yaxis_title="Average Delivery Days",
)

with left:

    with st.container(border=True):

        st.subheader("🚚 Delivery Days vs Rating")

        st.caption("Relationship between delivery speed and customer rating")

        st.plotly_chart(
            fig_delivery,
            use_container_width=True,
        )

state = run_query("""

SELECT

    c.customer_state,

    ROUND(
        AVG(r.review_score),
    2) AS avg_rating

FROM fact_reviews r

JOIN fact_orders o

ON r.order_id = o.order_id

JOIN dim_customer c

ON o.customer_id = c.customer_id

GROUP BY c.customer_state

ORDER BY avg_rating DESC

""")

fig_state = px.bar(
    state,
    x="customer_state",
    y="avg_rating",
    text="avg_rating",
    template="plotly_dark",
)

fig_state.update_traces(
    texttemplate="%{y:.2f}",
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
    yaxis_title="Average Rating",
)

with right:

    with st.container(border=True):

        st.subheader("🌎 Average Rating by State")

        st.caption("Average customer rating by state")

        st.plotly_chart(
            fig_state,
            use_container_width=True,
        )
