import streamlit as st

from src.services.application_tracker import save_job




def show_job_card(job):


    score = job.get(

        "match_score",

        0

    )


    level = job.get(

        "match_level",

        "Not ranked"

    )



    title = job.get(

        "job_title",

        "Unknown Position"

    )


    company = job.get(

        "company",

        "Unknown Company"

    )


    location = job.get(

        "location",

        ""

    )



    url = job.get(

        "url",

        ""

    )



    # Header

    st.subheader(
        title
    )


    st.write(
        f"🏢 {company}"
    )


    st.write(
        f"📍 {location}"
    )



    col1, col2 = st.columns(2)



    with col1:

        st.metric(

            "🎯 Match Score",

            f"{score}%"

        )



    with col2:

        st.info(
            level
        )





    # Explanation

    reason = job.get(

        "match_reason",

        ""

    )


    if reason:


        with st.expander(

            "🤖 Why this matches"

        ):

            st.write(
                reason
            )





    # Skills

    col1, col2 = st.columns(2)



    with col1:


        st.success(
            "✅ Matching Skills"
        )


        skills = job.get(

            "matched_skills",

            []

        )


        if skills:

            for skill in skills:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "No skills detected"
            )





    with col2:


        st.warning(
            "⚠️ Missing Skills"
        )


        missing = job.get(

            "missing_skills",

            []

        )


        if missing:

            for skill in missing:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "No missing skills"
            )





    # Description

    with st.expander(

        "📄 Job Description"

    ):


        description = job.get(

            "description",

            ""

        )


        if description:

            st.write(
                description
            )

        else:

            st.write(
                "Description not available"
            )





    # Actions

    col1, col2 = st.columns(2)



    with col1:


        if url:

            st.link_button(

                "🔗 Apply",

                url

            )




    with col2:


        if st.button(

            "❤️ Save Job",

            key=f"save_{url}"

        ):


            save_job(
                job
            )


            st.success(
                "Saved"
            )



    st.divider()