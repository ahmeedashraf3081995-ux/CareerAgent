import streamlit as st


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="CareerAgent",
    page_icon="💼",
    layout="wide"
)


# ============================================================
# Custom Styling
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       Sidebar Navigation
       ====================================================== */

    section[data-testid="stSidebar"] {

        width: 280px !important;

    }


    /* Sidebar navigation text */

    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] span {

        font-size: 18px !important;

        font-weight: 600 !important;

    }


    /* Sidebar navigation buttons */

    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] a {

        min-height: 48px !important;

    }


    /* CareerAgent title */

    section[data-testid="stSidebar"] h1 {

        font-size: 28px !important;

        font-weight: 700 !important;

    }


    /* Sidebar description */

    section[data-testid="stSidebar"] p {

        font-size: 15px !important;

    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# Navigation
# ============================================================

home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True
)


cv_search_page = st.Page(
    "pages/cv_search.py",
    title="CV Search",
    icon="📄"
)


cv_builder_page = st.Page(
    "pages/cv_builder.py",
    title="CV Builder",
    icon="✨"
)


manual_search_page = st.Page(
    "pages/manual_search.py",
    title="Manual Search",
    icon="🔎"
)


search_results_page = st.Page(
    "pages/search_results.py",
    title="Job Matches",
    icon="🎯"
)


# ============================================================
# Navigation
# ============================================================

pg = st.navigation(
    [
        home_page,
        cv_search_page,
        cv_builder_page,
        manual_search_page,
        search_results_page
    ]
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title(
        "💼 CareerAgent"
    )

    st.caption(
        "AI-Powered Job Search & CV Optimization"
    )


# ============================================================
# Run Application
# ============================================================

pg.run()