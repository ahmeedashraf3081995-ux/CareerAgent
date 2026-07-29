from src.scrapers.linkedin_scraper import (
    create_driver,
    extract_job_details
)



def load_descriptions(jobs):

    if not jobs:

        return jobs


    driver = None


    try:

        driver = create_driver()


        for index, job in enumerate(jobs):


            url = job.get(
                "url",
                ""
            )


            if not url:

                continue



            print(
                f"Loading description {index+1}/{len(jobs)}"
            )


            job["description"] = extract_job_details(

                driver,

                url

            )



    except Exception as e:


        print(
            "Description loader error:",
            e
        )



    finally:


        if driver:

            driver.quit()



    return jobs