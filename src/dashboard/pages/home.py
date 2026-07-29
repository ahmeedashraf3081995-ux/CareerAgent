import streamlit as st


st.set_page_config(
    page_title="CareerAgent",
    page_icon="💼",
    layout="wide"
)


st.title("💼 CareerAgent")

st.subheader(
    "AI-powered job search assistant"
)

st.write(
    """
Upload your CV and let AI find matching jobs,
or search manually by job title, location and company.
"""
)


st.divider()


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "## 📄 Search using CV"
    )

    st.write(
        "AI will analyze your CV and suggest suitable jobs."
    )


    if st.button(
        "Upload CV",
        use_container_width=True
    ):

        st.switch_page(
            "pages/cv_search.py"
        )



with col2:

    st.markdown(
        "## 🔎 Manual Search"
    )

    st.write(
        "Search without uploading any CV."
    )


    if st.button(
        "Manual Search",
        use_container_width=True
    ):

        st.switch_page(
            "pages/manual_search.py"
        )