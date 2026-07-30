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


pg.run()