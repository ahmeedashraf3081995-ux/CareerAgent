import streamlit as st

from src.dashboard.components.job_card import show_job_card



st.title(
    "🎯 CareerAgent Job Matches"
)



jobs = st.session_state.get(
    "jobs",
    []
)



if not jobs:

    st.warning(
        "No jobs found. Please run a search first."
    )

    st.stop()



# ==========================
# Sidebar Filters
# ==========================

st.sidebar.header(
    "🔎 Filters"
)



# Job Titles

job_titles = sorted(

    list(

        set(

            [

                job.get(
                    "job_title",
                    ""
                )

                for job in jobs

                if job.get(
                    "job_title"
                )

            ]

        )

    )

)



selected_titles = st.sidebar.multiselect(

    "Job Titles",

    job_titles

)




# Companies

companies = sorted(

    list(

        set(

            [

                job.get(
                    "company",
                    ""
                )

                for job in jobs

                if job.get(
                    "company"
                )

            ]

        )

    )

)



selected_companies = st.sidebar.multiselect(

    "Companies",

    companies

)





# Locations

locations = sorted(

    list(

        set(

            [

                job.get(
                    "location",
                    ""
                )

                for job in jobs

                if job.get(
                    "location"
                )

            ]

        )

    )

)



selected_locations = st.sidebar.multiselect(

    "Cities / Locations",

    locations

)





# Match score

minimum_score = st.sidebar.slider(

    "Minimum Match Score",

    min_value=0,

    max_value=100,

    value=0

)





# Sort

sort_option = st.sidebar.selectbox(

    "Sort By",

    [

        "Best Match",

        "Company",

        "Job Title"

    ]

)





# ==========================
# Apply Filters
# ==========================

filtered_jobs = []



for job in jobs:


    if selected_titles:

        if job.get(
            "job_title"
        ) not in selected_titles:

            continue



    if selected_companies:

        if job.get(
            "company"
        ) not in selected_companies:

            continue



    if selected_locations:

        if job.get(
            "location"
        ) not in selected_locations:

            continue



    if job.get(
        "match_score",
        0
    ) < minimum_score:

        continue



    filtered_jobs.append(
        job
    )





# ==========================
# Sorting
# ==========================

if sort_option == "Best Match":

    filtered_jobs.sort(

        key=lambda x: x.get(

            "match_score",

            0

        ),

        reverse=True

    )


elif sort_option == "Company":

    filtered_jobs.sort(

        key=lambda x: x.get(

            "company",

            ""

        )

    )


elif sort_option == "Job Title":

    filtered_jobs.sort(

        key=lambda x: x.get(

            "job_title",

            ""

        )

    )





st.success(

    f"{len(filtered_jobs)} jobs found"

)



st.divider()



for job in filtered_jobs:

    show_job_card(
        job
    )