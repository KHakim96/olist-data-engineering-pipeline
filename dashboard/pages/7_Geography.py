import streamlit as st
import plotly.express as px
import json
from pathlib import Path

from utils import run_query, load_css

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Geography Dashboard",
    page_icon="🌎",
    layout="wide",
)

load_css()

# ==========================================================
# LOAD BRAZIL MAP
# ==========================================================

geojson_path = Path(__file__).parent.parent / "assets" / "brazil_states.geojson"

with open(geojson_path) as f:
    brazil = json.load(f)

# ==========================================================
# HEADER
# ==========================================================

st.title("🌎 Geography Dashboard")
st.caption("Regional Business Performance")

st.divider()

##kpi

geo = run_query("""

SELECT

    COUNT(DISTINCT customer_state) AS states,

    COUNT(DISTINCT customer_city) AS cities,

    COUNT(DISTINCT customer_unique_id) AS customers,

    (
        SELECT COUNT(DISTINCT seller_id)
        FROM dim_seller
    ) AS sellers

FROM dim_customer

""")

row = geo.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        label="🌎 States",
        value=row.states,
        delta="Current",
    )

with c2:

    st.metric(
        label="🏙 Cities",
        value=f"{row.cities:,}",
        delta="Current",
    )

with c3:

    st.metric(
        label="👥 Customers",
        value=f"{row.customers/1000:.1f}K",
        delta="Current",
    )

with c4:

    st.metric(
        label="🏪 Sellers",
        value=f"{row.sellers:,}",
        delta="Current",
    )

st.write("")

## revenue by state

state = run_query("""

SELECT
    oi.seller_state,

    SUM(oi.price) AS revenue,

    COUNT(DISTINCT oi.order_id) AS orders,

    COUNT(DISTINCT o.customer_id) AS customers,

    ROUND(AVG(r.review_score),2) AS avg_rating

FROM fact_order_items oi

JOIN fact_orders o
ON oi.order_id = o.order_id

LEFT JOIN fact_reviews r
ON oi.order_id = r.order_id

GROUP BY oi.seller_state

""")


fig_map = px.choropleth(
    state,
    geojson=brazil,
    locations="seller_state",
    featureidkey="properties.sigla",
    color="revenue",
    color_continuous_scale="Blues",
    hover_name="seller_state",
    hover_data={
        "revenue": ":,.0f",
        "orders": ":,.0f",
        "customers": ":,.0f",
        "avg_rating": ":.2f",
    },
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="#0E1117",
    showland=True,
    # landcolor="#1F2937",
    landcolor="#111827",
    showcountries=False,
    showcoastlines=False,
    showlakes=False,
    showocean=False,
)


fig_map.update_layout(
    height=650,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(
        l=0,
        r=0,
        t=10,
        b=0,
    ),
    coloraxis_colorbar=dict(
        title="Revenue",
        tickfont=dict(color="white"),
        title_font=dict(color="white"),
    ),
)

with st.container(border=True):

    st.subheader("🗺 Revenue by State")

    st.caption("Interactive Brazil revenue heatmap")

    st.plotly_chart(
        fig_map,
        use_container_width=True,
    )

##👥 Customers by State      🏪 Sellers by State

left, right = st.columns(2, gap="large")

customers = run_query("""

SELECT

    customer_state,

    COUNT(DISTINCT customer_unique_id) AS customers

FROM dim_customer

GROUP BY customer_state

ORDER BY customers DESC

""")

fig_customers = px.bar(
    customers,
    x="customer_state",
    y="customers",
    text="customers",
    template="plotly_dark",
)

fig_customers.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#3B82F6",
)

fig_customers.update_layout(
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

        st.subheader("👥 Customers by State")

        st.caption("Unique customers by state")

        st.plotly_chart(
            fig_customers,
            use_container_width=True,
        )

sellers = run_query("""

SELECT

    seller_state,

    COUNT(DISTINCT seller_id) AS sellers

FROM dim_seller

GROUP BY seller_state

ORDER BY sellers DESC

""")

fig_sellers = px.bar(
    sellers,
    x="seller_state",
    y="sellers",
    text="sellers",
    template="plotly_dark",
)

fig_sellers.update_traces(
    texttemplate="%{y:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#10B981",
)

fig_sellers.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis_title="",
    yaxis_title="Sellers",
)

with right:

    with st.container(border=True):

        st.subheader("🏪 Sellers by State")

        st.caption("Registered sellers by state")

        st.plotly_chart(
            fig_sellers,
            use_container_width=True,
        )

##🏙 Top Customer Cities      🏭 Top Seller Cities

left, right = st.columns(2, gap="large")

cities = run_query("""

SELECT

    customer_city,

    COUNT(DISTINCT customer_unique_id) AS customers

FROM dim_customer

GROUP BY customer_city

ORDER BY customers DESC

LIMIT 10

""")

fig_city = px.bar(
    cities,
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
    marker_color="#F59E0B",
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

with left:

    with st.container(border=True):

        st.subheader("🏙 Top Customer Cities")

        st.caption("Top 10 cities by customer count")

        st.plotly_chart(
            fig_city,
            use_container_width=True,
        )

seller_city = run_query("""

SELECT

    seller_city,

    COUNT(DISTINCT seller_id) AS sellers

FROM dim_seller

GROUP BY seller_city

ORDER BY sellers DESC

LIMIT 10

""")

fig_seller_city = px.bar(
    seller_city,
    x="sellers",
    y="seller_city",
    orientation="h",
    text="sellers",
    template="plotly_dark",
)

fig_seller_city.update_traces(
    texttemplate="%{x:,.0f}",
    textposition="outside",
    cliponaxis=False,
    marker_color="#EF4444",
)

fig_seller_city.update_layout(
    height=420,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    margin=dict(l=10, r=40, t=10, b=10),
    xaxis_title="Sellers",
    yaxis_title="",
    yaxis=dict(categoryorder="total ascending"),
)

with right:

    with st.container(border=True):

        st.subheader("🏭 Top Seller Cities")

        st.caption("Top 10 cities by seller count")

        st.plotly_chart(
            fig_seller_city,
            use_container_width=True,
        )
