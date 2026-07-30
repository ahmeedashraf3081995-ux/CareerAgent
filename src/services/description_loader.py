from src.scrapers.linkedin_scraper import extract_job_details
import time


def load_descriptions(
    jobs,
    limit=30
):

    """
    Load real LinkedIn job descriptions.

    Only the first `limit` jobs are opened
    to protect Streamlit Cloud resources.
    """

    loaded = 0


    for job in jobs:

        # --------------------------------------
        # Stop after limit
        # --------------------------------------

        if loaded >= limit:

            break


        # --------------------------------------
        # Skip if description already exists
        # --------------------------------------

        existing_description = job.get(
            "description",
            ""
        )


        if existing_description:

            continue


        # --------------------------------------
        # Get URL
        # --------------------------------------

        url = job.get(
            "url",
            ""
        )


        if not url:

            job["description"] = ""

            continue


        try:

            print(
                f"Loading description {loaded + 1}/{limit}"
            )


            description = extract_job_details(
                url
            )


            job["description"] = description


            if description:

                loaded += 1


            # Small delay to avoid
            # hammering LinkedIn

            time.sleep(0.3)


        except Exception as e:

            print(
                "Description error:",
                e
            )


            job["description"] = ""


    # --------------------------------------
    # Ensure every job has description field
    # --------------------------------------

    for job in jobs:

        if "description" not in job:

            job["description"] = ""


    print(
        f"Descriptions successfully loaded: {loaded}"
    )


    return jobs