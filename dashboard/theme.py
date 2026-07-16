import streamlit as st


def configure_page():
    st.set_page_config(
        page_title="OLIST Enterprise Analytics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme():
    st.markdown(
        """
<style>

/* ---------- Global ---------- */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
    padding-bottom:2rem;
}

/* ---------- Headings ---------- */

h1{
    font-size:40px;
    font-weight:700;
    margin-bottom:0.2rem;
}

h2{
    font-size:28px;
    font-weight:700;
}

h3{
    font-size:22px;
    font-weight:600;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    border-right:1px solid rgba(255,255,255,.08);
}

/* ---------- Metric ---------- */

div[data-testid="metric-container"]{

    background:rgba(255,255,255,.04);

    border:1px solid rgba(255,255,255,.08);

    border-radius:18px;

    padding:20px;

    transition:0.25s;
}

div[data-testid="metric-container"]:hover{

    transform:translateY(-4px);

    border:1px solid #2563EB;

}

/* ---------- Buttons ---------- */

.stButton>button{

    border-radius:12px;

}

/* ---------- Footer ---------- */

footer{

    visibility:hidden;

}

/* ---------- Main Menu ---------- */

#MainMenu{

    visibility:hidden;

}

</style>
""",
        unsafe_allow_html=True,
    )
