import streamlit as st

from services.application_tracker import (
    save_job,
    update_job_status
)




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


    job_id = (

        url

        or

        (

            title

            +

            company

        )

    )



    # ==========================
    # Header
    # ==========================


    st.subheader(
        title
    )


    st.write(
        f"🏢 **{company}**"
    )


    st.write(
        f"📍 {location}"
    )



    col1, col2 = st.columns(2)



    with col1:

        st.metric(

            "🎯 CV Match",

            f"{score}%"

        )



    with col2:

        st.info(
            level
        )





    # ==========================
    # Match Explanation
    # ==========================


    reason = job.get(

        "match_reason",

        ""

    )


    if reason:


        with st.expander(

            "🤖 Why this job matches you"

        ):


            st.write(
                reason
            )





    # ==========================
    # Skills
    # ==========================


    col1, col2 = st.columns(2)



    with col1:


        st.success(
            "✅ Matching Skills"
        )


        matched = job.get(

            "matched_skills",

            []

        )


        if matched:


            for skill in matched:


                st.write(

                    f"✓ {skill}"

                )


        else:


            st.write(
                "No strong overlap found"
            )





    with col2:


        st.warning(
            "⚠️ Skills To Improve"
        )


        missing = job.get(

            "missing_skills",

            []

        )


        if missing:


            for skill in missing:


                st.write(

                    f"+ {skill}"

                )


        else:


            st.write(
                "No missing skills"
            )





    # ==========================
    # Description
    # ==========================


    with st.expander(

        "📄 Full Job Description"

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


            st.warning(
                "Description not available"
            )





    # ==========================
    # Actions
    # ==========================


    col1, col2, col3 = st.columns(3)



    with col1:


        if url:


            st.link_button(

                "🔗 Apply",

                url

            )





    with col2:


        if st.button(

            "❤️ Save",

            key=f"save_{job_id}"

        ):


            saved = save_job(
                job
            )


            if saved:


                st.success(
                    "Saved"
                )

            else:


                st.info(
                    "Already saved"
                )





    with col3:


        status = st.selectbox(

            "Status",

            [

                "❤️ Saved",

                "📩 Applied",

                "🗣 Interview",

                "✅ Offer",

                "❌ Rejected"

            ],

            key=f"status_{job_id}"

        )



        if st.button(

            "Update",

            key=f"update_{job_id}"

        ):


            update_job_status(

                job_id,

                status

            )


            st.success(
                "Status updated"
            )





    st.divider()