import streamlit as st
import sys
import os
import hashlib


# ==================================================
# Project Root
# ==================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../.."
        )
    )
)


# ==================================================
# Services
# ==================================================

from src.services.cv_parser import extract_text
from src.services.cv_analyzer import analyze_cv
from src.services.job_search import search_jobs
from src.services.job_matcher import match_jobs
from src.services.cv_job_analyzer import analyze_jobs_against_cv
from src.services.job_ranker import rank_jobs_with_ai


# ==================================================
# Components
# ==================================================

from components.chips import tag_input


# ==================================================
# Page Header
# ==================================================

st.title(
    "📄 CV-Based Job Search"
)

st.write(
    "Upload Your CV And CareerAgent Will Analyze It "
    "And Suggest The Best Job Search Criteria."
)


# ==================================================
# Upload CV
# ==================================================

uploaded_file = st.file_uploader(
    "Upload Your CV",
    type=["pdf"]
)


if uploaded_file:

    # ==================================================
    # Identify Uploaded CV
    # ==================================================

    file_bytes = uploaded_file.getvalue()

    current_file_id = hashlib.md5(
        file_bytes
    ).hexdigest()


    # ==================================================
    # Detect New CV
    # ==================================================

    if st.session_state.get(
        "uploaded_cv_id"
    ) != current_file_id:

        clear_keys = [

            "cv_text",

            "cv_job_titles",
            "cv_countries",
            "cv_cities",
            "cv_companies",

            "cv_job_titles_input",
            "cv_countries_input",
            "cv_cities_input",
            "cv_companies_input",

            "jobs",
            "search_parameters"

        ]

        for key in clear_keys:

            st.session_state.pop(
                key,
                None
            )

        st.session_state.uploaded_cv_id = (
            current_file_id
        )


    # ==================================================
    # Analyze CV
    # ==================================================

    if "cv_text" not in st.session_state:

        with st.spinner(
            "Analyzing CV..."
        ):

            text = extract_text(
                uploaded_file
            )

            analysis = analyze_cv(
                text
            )

            st.session_state.cv_text = (
                text
            )

            st.session_state.cv_job_titles = (
                analysis.get(
                    "job_titles",
                    []
                )
            )

            st.session_state.cv_countries = (
                analysis.get(
                    "countries",
                    []
                )
            )

            st.session_state.cv_cities = (
                analysis.get(
                    "cities",
                    []
                )
            )

            st.session_state.cv_companies = []


        st.success(
            "CV Successfully Analyzed"
        )

    else:

        st.success(
            "CV Successfully Analyzed"
        )


    # ==================================================
    # CV Content
    # ==================================================

    with st.expander(
        "Extracted CV Content"
    ):

        st.text(
            st.session_state.cv_text
        )


    st.divider()


    # ==================================================
    # Search Preferences
    # ==================================================

    st.subheader(
        "🎯 Search Preferences"
    )

    st.info(
        "CareerAgent Generated These Suggestions From Your CV. "
        "Edit, Remove, Or Add Anything Before Searching."
    )


    # ==================================================
    # Editable Filters
    # ==================================================

    job_titles = tag_input(
        "Job Titles",
        "cv_job_titles"
    )

    countries = tag_input(
        "Countries",
        "cv_countries"
    )

    cities = tag_input(
        "Cities",
        "cv_cities"
    )

    companies = tag_input(
        "Companies",
        "cv_companies"
    )


    # ==================================================
    # Job Posting Date
    # ==================================================

    posted_days = st.selectbox(

        "📅 Job Posting Date",

        options=[
            1,
            3,
            7,
            14,
            30,
            0
        ],

        format_func=lambda x:

            (
                "Last 1 day"
                if x == 1

                else

                "Last 3 days"
                if x == 3

                else

                "Last 7 days"
                if x == 7

                else

                "Last 14 days"
                if x == 14

                else

                "Last 30 days"
                if x == 30

                else

                "Any time"
            ),

        index=2

    )


    st.divider()


    # ==================================================
    # Search
    # ==================================================

    if st.button(
        "🚀 Find Matching Jobs",
        use_container_width=True
    ):

        if not job_titles:

            st.warning(
                "Please Add At Least One Job Title."
            )

        else:

            # ==========================================
            # Search Parameters
            # ==========================================

            search_parameters = {

                "job_titles":
                    job_titles,

                "countries":
                    countries,

                "cities":
                    cities,

                "companies":
                    companies,

                "posted_days":
                    posted_days,

                "cv_text":
                    st.session_state.cv_text

            }


            st.session_state.search_parameters = (
                search_parameters
            )


            # ==========================================
            # Search Jobs
            # ==========================================

            with st.spinner(
                "Searching Jobs..."
            ):

                jobs = search_jobs(
                    search_parameters
                )


            st.success(
                f"Found {len(jobs)} Jobs"
            )


            # ==========================================
            # Match Jobs With CV
            # ==========================================

            with st.spinner(
                "Matching Jobs With CV..."
            ):

                matched_jobs = match_jobs(

                    st.session_state.cv_text,

                    jobs

                )


            # ==========================================
            # AI JOB ANALYSIS + RANKING
            # ==========================================

            with st.spinner(
                "🤖 AI Is Analyzing And Ranking Jobs..."
            ):

                matched_jobs = rank_jobs_with_ai(

                    st.session_state.cv_text,

                    matched_jobs

                )


            # ==========================================
            # Generate CV-Based Analysis
            # ==========================================

            with st.spinner(
                "Generating CV Recommendations..."
            ):

                matched_jobs = (
                    analyze_jobs_against_cv(

                        st.session_state.cv_text,

                        matched_jobs

                    )
                )


            # ==========================================
            # Save Final Results
            # ==========================================

            st.session_state.jobs = (
                matched_jobs
            )


            # ==========================================
            # Go To Results
            # ==========================================

            st.switch_page(
                "pages/search_results.py"
            )