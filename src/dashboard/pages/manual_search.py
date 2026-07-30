import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../.."
        )
    )
)

import streamlit as st

from components.chips import tag_input
from src.services.job_search import search_jobs


# ==================================================
# Page Header
# ==================================================

st.title(
    "🔎 Manual Job Search"
)

st.write(
    "Define What Jobs You Want CareerAgent To Search For."
)


# ==================================================
# Inputs
# ==================================================

job_titles = tag_input(
    "Job Titles",
    "job_titles"
)


countries = tag_input(
    "Countries",
    "countries"
)


cities = tag_input(
    "Cities",
    "cities"
)


companies = tag_input(
    "Companies",
    "companies"
)


keywords = tag_input(
    "Keywords",
    "keywords"
)


st.divider()


# ==================================================
# Search Button
# ==================================================

if st.button(
    "🚀 Search Jobs",
    use_container_width=True
):

    parameters = {

        "job_titles": job_titles,

        "countries": countries,

        "cities": cities,

        "companies": companies,

        "keywords": keywords

    }


    st.session_state[
        "search_parameters"
    ] = parameters


    if not job_titles:

        st.warning(
            "Please Add At Least One Job Title."
        )

    else:

        with st.spinner(
            "Searching LinkedIn Jobs..."
        ):

            results = search_jobs(
                parameters
            )


        st.session_state[
            "jobs"
        ] = results


        st.success(
            f"Found {len(results)} Jobs"
        )


        st.switch_page(
            "pages/search_results.py"
        )