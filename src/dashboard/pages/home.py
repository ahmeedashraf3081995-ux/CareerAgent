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
# Header
# ==================================================

st.title(
    "💼 CareerAgent"
)

st.subheader(
    "AI-Powered Job Search Assistant"
)

st.write(
    """
Upload Your CV And Let AI Find Matching Jobs,
Or Search Manually By Job Title, Location, And Company.
"""
)


st.divider()


# ==================================================
# Search Options
# ==================================================

col1, col2 = st.columns(2)


# ==================================================
# CV Search
# ==================================================

with col1:

    st.markdown(
        "## 📄 Search Using CV"
    )

    st.write(
        "AI Will Analyze Your CV And Suggest Suitable Jobs."
    )

    if st.button(
        "Upload CV",
        use_container_width=True
    ):

        st.switch_page(
            "pages/cv_search.py"
        )


# ==================================================
# Manual Search
# ==================================================

with col2:

    st.markdown(
        "## 🔎 Manual Search"
    )

    st.write(
        "Search Without Uploading A CV."
    )

    if st.button(
        "Manual Search",
        use_container_width=True
    ):

        st.switch_page(
            "pages/manual_search.py"
        )