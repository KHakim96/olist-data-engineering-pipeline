from pathlib import Path

import duckdb
import pandas as pd

import streamlit as st

DB_PATH = Path(__file__).parent.parent / "warehouse" / "olist.duckdb"


def run_query(sql: str) -> pd.DataFrame:
    """
    Execute SQL against DuckDB and return a DataFrame.
    """

    conn = duckdb.connect(DB_PATH)

    try:
        return conn.execute(sql).df()

    finally:
        conn.close()


########


def load_css():
    st.markdown(
        """
<style>

/* ===========================
Main Layout
=========================== */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
    padding-bottom:2rem;
    max-width:1600px;
}

/* ===========================
Metric Cards
=========================== */

div[data-testid="stMetric"]{

    background:#1F2937;

    border:1px solid #374151;

    border-radius:18px;

    padding:22px;

    box-shadow:0 8px 25px rgba(0,0,0,.30);

}

/* Label */

div[data-testid="stMetricLabel"]{

    color:#9CA3AF !important;

    font-size:15px;

}

/* Value */

div[data-testid="stMetricValue"]{

    color:white !important;

    font-size:38px;

    font-weight:700;

}

/* Delta */

div[data-testid="stMetricDelta"]{

    color:#22C55E !important;

    font-weight:600;

}

/* ===========================
Containers
=========================== */

div[data-testid="stVerticalBlock"]>div:has(div[data-testid="stPlotlyChart"]){

    border-radius:18px;

}

/* ===========================
Headings
=========================== */

h1{

    font-size:44px;

    font-weight:700;

}

h2{

    font-size:28px;

}

h3{

    font-size:22px;

}

/* ===========================
Sidebar
=========================== */

section[data-testid="stSidebar"]{

    background:#111827;

}

/* ===========================
Hide Streamlit Footer
=========================== */

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
