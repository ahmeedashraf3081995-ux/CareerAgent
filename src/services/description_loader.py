from src.scrapers.linkedin_scraper import extract_job_details
import time


# ==================================================
# Load Job Descriptions
# ==================================================

def load_descriptions(jobs):

    """
    Load LinkedIn descriptions for all jobs.

    Every job returned to the matching stage will have
    a description field, even if LinkedIn fails to provide
    one.
    """

    total = len(jobs)

    loaded = 0

    failed = 0


    for index, job in enumerate(jobs, start=1):

        url = job.get(
            "url",
            ""
        )


        # ------------------------------------------
        # Ensure Description Field Exists
        # ------------------------------------------

        if not url:

            job["description"] = ""

            failed += 1

            continue


        try:

            print(
                f"Loading description {index}/{total}"
            )


            description = extract_job_details(
                url
            )


            if description:

                job["description"] = description

                loaded += 1

            else:

                job["description"] = ""

                failed += 1


            # --------------------------------------
            # Small Delay Between Requests
            # --------------------------------------

            time.sleep(
                0.5
            )


        except Exception as e:

            print(
                "Description error:",
                e
            )


            job["description"] = ""

            failed += 1


    # ==================================================
    # Final Safety Check
    # ==================================================

    for job in jobs:

        if "description" not in job:

            job["description"] = ""


    print(
        "Descriptions loaded:",
        loaded
    )


    print(
        "Descriptions unavailable:",
        failed
    )


    print(
        "Total jobs processed:",
        total
    )


    return jobs