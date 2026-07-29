from src.scrapers.linkedin_scraper import extract_job_details
import time




def load_descriptions(jobs, limit=50):


    """

    Load LinkedIn descriptions.

    Limited to protect Streamlit Cloud resources.

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



            # avoid hammering LinkedIn

            time.sleep(0.5)



        except Exception as e:


            print(

                "Description error:",

                e

            )


            job["description"] = ""





    # Ensure field exists

    for job in jobs:


        if "description" not in job:

            job["description"] = ""



    return jobs