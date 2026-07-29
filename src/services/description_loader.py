from src.scrapers.linkedin_scraper import extract_job_details



def load_descriptions(jobs, limit=30):

    """
    Load job descriptions from LinkedIn.

    We limit extraction to avoid CPU overload
    on Streamlit Cloud while keeping results.
    """

    loaded = 0


    for job in jobs:


        if loaded >= limit:

            break



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



            loaded += 1



        except Exception as e:


            print(

                "Description loader error:",

                e

            )


            job["description"] = ""




    # Make sure every job has the field

    for job in jobs:


        if "description" not in job:


            job["description"] = ""



    return jobs