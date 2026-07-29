import streamlit as st

st.set_page_config(
    page_title="CareerAgent",
    page_icon="💼",
    layout="wide"
)

st.title("💼 CareerAgent")

st.markdown(
    """
## AI-Powered Job Search

Upload your CV for AI recommendations or search manually.
"""
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload CV")

    st.write(
        "Upload your CV and let AI detect your skills before searching."
    )

    if st.button(
        "Start with CV",
        use_container_width=True
    ):
        st.switch_page("pages/cv_search.py")


with col2:
    st.subheader("✏️ Manual Search")

    st.write(
        "Search jobs without uploading a CV."
    )

    if st.button(
        "Search Manually",
        use_container_width=True
    ):
        st.switch_page("pages/manual_search.py")