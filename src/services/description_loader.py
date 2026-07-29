from src.scrapers.linkedin_scraper import create_driver
from src.scrapers.linkedin_scraper import extract_job_description





def load_descriptions(jobs):


    driver = create_driver()



    try:


        for job in jobs:


            if job.get(
                "url"
            ):


                print(
                    "Reading:",
                    job.get(
                        "job_title"
                    )
                )


                job["description"] = extract_job_description(

                    driver,

                    job["url"]

                )



    finally:


        driver.quit()



    return jobs