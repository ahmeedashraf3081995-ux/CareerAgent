import streamlit as st
import sys
import os
import hashlib


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../.."
        )
    )
)


from src.services.cv_parser import extract_text
from src.services.cv_analyzer import analyze_cv
from src.services.job_search import search_jobs
from src.services.job_matcher import match_jobs

from components.chips import tag_input



st.title("📄 CV Based Job Search")


st.write(
    "Upload your CV and CareerAgent will analyze it and suggest the best job search criteria."
)



# ==========================
# Upload CV
# ==========================

uploaded_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"]
)



if uploaded_file:


    file_bytes = uploaded_file.getvalue()


    current_file_id = hashlib.md5(
        file_bytes
    ).hexdigest()



    # ==========================
    # Detect new CV
    # ==========================

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
            "cv_companies_input"

        ]


        for key in clear_keys:

            st.session_state.pop(
                key,
                None
            )



        st.session_state.uploaded_cv_id = current_file_id



    # ==========================
    # Analyze CV
    # ==========================

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



            st.session_state.cv_text = text



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
        "CV successfully analyzed"
    )



    # ==========================
    # CV Content
    # ==========================

    with st.expander(
        "Extracted CV Content"
    ):

        st.text(
            st.session_state.cv_text
        )



    st.divider()



    st.subheader(
        "🎯 Search Preferences"
    )


    st.info(
        "CareerAgent generated these suggestions from your CV. Edit, remove, or add anything before searching."
    )



    # ==========================
    # Editable Filters
    # ==========================

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



    st.divider()



    # ==========================
    # Search
    # ==========================

    if st.button(
        "🚀 Find Matching Jobs",
        use_container_width=True
    ):



        if not job_titles:


            st.warning(
                "Please add at least one job title."
            )


        else:



            search_parameters = {

                "job_titles": job_titles,

                "countries": countries,

                "cities": cities,

                "companies": companies,

                "cv_text": st.session_state.cv_text

            }



            st.session_state.search_parameters = search_parameters



            with st.spinner(
                "Searching jobs..."
            ):


                jobs = search_jobs(
                    search_parameters
                )



            st.success(
                f"Found {len(jobs)} jobs"
            )



            with st.spinner(
                "Matching jobs with CV..."
            ):


                matched_jobs = match_jobs(
                    st.session_state.cv_text,
                    jobs
                )



            st.session_state.jobs = matched_jobs



            st.switch_page(
                "pages/search_results.py"
            )