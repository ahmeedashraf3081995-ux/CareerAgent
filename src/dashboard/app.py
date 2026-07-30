import streamlit as st


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="CareerAgent",
    page_icon="💼",
    layout="wide"
)


# ==================================================
# Navigation
# ==================================================

pages = {

    "CareerAgent": [

        st.Page(
            "pages/home.py",
            title="Home",
            icon="🏠"
        ),

        st.Page(
            "pages/cv_search.py",
            title="CV Search",
            icon="📄"
        ),

        st.Page(
            "pages/manual_search.py",
            title="Manual Search",
            icon="🔎"
        ),

        st.Page(
            "pages/search_results.py",
            title="Search Results",
            icon="🎯"
        )

    ]

}


pg = st.navigation(
    pages
)


pg.run()