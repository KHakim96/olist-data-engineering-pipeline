import streamlit as st


def page_header(title, subtitle):
    st.markdown(
        f"""
        <div style="margin-bottom:30px;">
            <h1 style="margin-bottom:0;">{title}</h1>
            <p style="color:#94A3B8;font-size:18px;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    st.markdown("<hr>", unsafe_allow_html=True)


def metric_card(title, value, delta, icon):

    st.markdown(
        f"""
        <div style="
            background:#1E293B;
            padding:22px;
            border-radius:18px;
            border:1px solid #334155;
            box-shadow:0 4px 15px rgba(0,0,0,.25);
            height:165px;
        ">

            <div style="font-size:30px;">
                {icon}
            </div>

            <div style="
                color:#94A3B8;
                font-size:15px;
                margin-top:8px;
            ">
                {title}
            </div>

            <div style="
                font-size:38px;
                font-weight:700;
                margin-top:8px;
            ">
                {value}
            </div>

            <div style="
                color:#10B981;
                margin-top:8px;
                font-size:16px;
            ">
                ▲ {delta}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title):

    st.markdown(
        f"""
        <h2 style="margin-top:20px;">
            {title}
        </h2>
        """,
        unsafe_allow_html=True,
    )


def chart_placeholder(height=350):

    st.markdown(
        f"""
        <div style="
            height:{height}px;
            border-radius:18px;
            background:#172554;
            border:1px dashed #3B82F6;
            display:flex;
            align-items:center;
            justify-content:center;
            color:white;
            font-size:18px;
        ">
            📈 Plotly Chart Coming Soon
        </div>
        """,
        unsafe_allow_html=True,
    )


def pipeline_status():

    st.markdown(
        """
        <div style="
            background:#1E293B;
            border-radius:18px;
            padding:20px;
            border:1px solid #334155;
        ">

        <h3>Pipeline Health</h3>

        🟢 PostgreSQL<br><br>

        🟢 Parquet Data Lake<br><br>

        🟢 DuckDB Warehouse<br><br>

        🟢 dbt Models<br><br>

        🟢 Airflow Orchestration

        </div>
        """,
        unsafe_allow_html=True,
    )
