import streamlit as st

from components.job_card import show_job_card



st.title(
    "📌 CareerAgent Job Matches"
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



# ==================================================
# Dashboard Summary
# ==================================================

st.subheader(
    "📊 Search Summary"
)



total_jobs = len(jobs)



excellent = len(
    [
        j for j in jobs
        if "Excellent" in j.get(
            "match_level",
            ""
        )
    ]
)



good = len(
    [
        j for j in jobs
        if "Good" in j.get(
            "match_level",
            ""
        )
    ]
)



partial = len(
    [
        j for j in jobs
        if "Partial" in j.get(
            "match_level",
            ""
        )
    ]
)



average_score = round(

    sum(

        j.get(
            "match_score",
            0
        )

        for j in jobs

    )

    /

    len(jobs)

)



col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(

        "📄 Total Jobs",

        total_jobs

    )



with col2:

    st.metric(

        "🔥 Excellent",

        excellent

    )



with col3:

    st.metric(

        "✅ Good",

        good

    )



with col4:

    st.metric(

        "📈 Avg Score",

        f"{average_score}%"

    )




st.divider()



# ==================================================
# Sidebar Filters
# ==================================================

st.sidebar.header(
    "🔎 Filters"
)



# --------------------------
# Job Title
# --------------------------

job_titles = sorted(

    list(

        set(

            [

                j.get(
                    "job_title",
                    ""
                )

                for j in jobs

                if j.get(
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




# --------------------------
# Companies
# --------------------------

companies = sorted(

    list(

        set(

            [

                j.get(
                    "company",
                    ""
                )

                for j in jobs

                if j.get(
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





# --------------------------
# Locations
# --------------------------

locations = sorted(

    list(

        set(

            [

                j.get(
                    "location",
                    ""
                )

                for j in jobs

                if j.get(
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





# --------------------------
# Match Level
# --------------------------

levels = sorted(

    list(

        set(

            [

                j.get(
                    "match_level",
                    ""
                )

                for j in jobs

                if j.get(
                    "match_level"
                )

            ]

        )

    )

)



selected_levels = st.sidebar.multiselect(

    "Match Level",

    levels

)





# --------------------------
# Score Slider
# --------------------------

minimum_score = st.sidebar.slider(

    "Minimum Match Score",

    0,

    100,

    0

)




# --------------------------
# Sorting
# --------------------------

sort_option = st.sidebar.selectbox(

    "Sort By",

    [

        "Best Match",

        "Highest Score",

        "Company",

        "Job Title"

    ]

)





# ==================================================
# Apply Filters
# ==================================================

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




    if selected_levels:


        if job.get(
            "match_level"
        ) not in selected_levels:


            continue




    if job.get(

        "match_score",

        0

    ) < minimum_score:


        continue




    filtered_jobs.append(
        job
    )





# ==================================================
# Sorting
# ==================================================

if sort_option in [

    "Best Match",

    "Highest Score"

]:


    filtered_jobs.sort(

        key=lambda x:

        x.get(

            "match_score",

            0

        ),

        reverse=True

    )



elif sort_option == "Company":


    filtered_jobs.sort(

        key=lambda x:

        x.get(

            "company",

            ""

        )

    )



elif sort_option == "Job Title":


    filtered_jobs.sort(

        key=lambda x:

        x.get(

            "job_title",

            ""

        )

    )





# ==================================================
# Results
# ==================================================

st.success(

    f"{len(filtered_jobs)} jobs displayed"

)



st.divider()



if not filtered_jobs:


    st.warning(
        "No jobs match your filters."
    )



else:


    for job in filtered_jobs:


        show_job_card(
            job
        )