import json
import os

from datetime import datetime


from .amazon_scraper import scrape_amazon
from .pg_scraper import scrape_pg
from .unilever_scraper import scrape_unilever
from .samsung_scraper import scrape_samsung
from .linkedin_scraper import scrape_linkedin

from ai.job_search_generator import generate_job_search



OUTPUT = "data/jobs/jobs_database.json"







def clean_location(job):

    location = job.get(
        "location",
        ""
    )


    if not location or location.lower() == "global":

        text = (
            job.get("job_title", "")
            +
            " "
            +
            job.get("description", "")
        ).lower()


        if "dubai" in text:
            location = "Dubai, UAE"

        elif "london" in text:
            location = "London, UK"

        elif "seattle" in text:
            location = "Seattle, USA"

        elif "france" in text:
            location = "France"

        elif "luxembourg" in text:
            location = "Luxembourg"

        else:
            location = "Not Specified"


    job["location"] = location


    return job








def filter_relevant_jobs(
    jobs,
    search_keywords=None
):

    if not search_keywords:

        return jobs



    filtered = []



    for job in jobs:


        text = (

            job.get(
                "job_title",
                ""
            )

            +

            " "

            +

            job.get(
                "description",
                ""
            )

        ).lower()



        for keyword in search_keywords:


            if keyword.lower() in text:


                filtered.append(job)

                break



    return filtered








def remove_duplicates(jobs):


    unique = {}



    for job in jobs:


        key = (

            job.get("company"),

            job.get("job_title"),

            job.get("location")

        )


        unique[key] = job



    return list(
        unique.values()
    )










def add_metadata(jobs):


    for job in jobs:


        clean_location(job)



        if "scraped_date" not in job:


            job["scraped_date"] = str(
                datetime.now()
            )



        if "source" not in job:


            job["source"] = "Unknown"



    return jobs










def run_scrapers(profile=None):


    print(
        "Starting Job Scraper Engine...\n"
    )



    jobs = []






    # =========================
    # Generate AI Search Terms
    # =========================


    if profile:


        print(
            "\nGenerating AI job keywords..."
        )


        try:


            search_result = generate_job_search(
                profile
            )


            search_keywords = search_result.get(
                "search_keywords",
                []
            )


            exclude_keywords = search_result.get(
                "exclude_keywords",
                []
            )


            print(
                "AI Search Keywords:",
                search_keywords
            )


        except Exception as e:


            print(
                "AI generation error:",
                e
            )


            search_keywords = [

                "Supply Chain Coordinator",

                "Procurement Assistant",

                "Inventory Coordinator"

            ]


            exclude_keywords = []



    else:


        print(
            "No CV profile received"
        )


        search_keywords = [

            "Supply Chain Coordinator",

            "Procurement Assistant"

        ]


        exclude_keywords = []









    # =========================
    # Company Scrapers
    # =========================


    scrapers = [

        ("Amazon", scrape_amazon),

        ("P&G", scrape_pg),

        ("Unilever", scrape_unilever),

        ("Samsung", scrape_samsung)

    ]





    for name, scraper in scrapers:


        print(
            "Running",
            name
        )


        try:


            result = scraper()


            print(

                name,

                "jobs:",

                len(result)

            )


            jobs.extend(result)



        except Exception as e:


            print(

                name,

                "error:",

                e

            )









    # =========================
    # LinkedIn
    # =========================


    print(
        "\nRunning LinkedIn..."
    )



    linkedin_jobs = []



    try:


        # Only search top 3 AI-generated titles

        top_keywords = search_keywords[:3]


        print(
            "LinkedIn titles:",
            top_keywords
        )


        for keyword in top_keywords:


            print(

                "\nLinkedIn search:",

                keyword

            )



            result = scrape_linkedin(

                keyword=keyword,

                location="Dubai"

            )



            print(

                keyword,

                "found:",

                len(result)

            )



            linkedin_jobs.extend(
                result
            )



        jobs.extend(
            linkedin_jobs
        )



    except Exception as e:


        print(
            "LinkedIn error:",
            e
        )









    print(

        "\nBefore filtering:",

        len(jobs)

    )






    # CV based filtering

    jobs = filter_relevant_jobs(

        jobs,

        top_keywords

    )



    print(

        "After relevance filter:",

        len(jobs)

    )










    # Remove excluded seniority jobs

    if exclude_keywords:


        filtered = []



        for job in jobs:


            title = job.get(

                "job_title",

                ""

            ).lower()



            if any(

                word.lower() in title

                for word in exclude_keywords

            ):

                continue



            filtered.append(job)



        jobs = filtered



    print(

        "After seniority filter:",

        len(jobs)

    )








    jobs = remove_duplicates(
        jobs
    )



    print(

        "After duplicate removal:",

        len(jobs)

    )






    jobs = add_metadata(
        jobs
    )







    os.makedirs(

        "data/jobs",

        exist_ok=True

    )






    with open(

        OUTPUT,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            jobs,

            f,

            indent=2,

            ensure_ascii=False

        )






    print(
        "\nScraping completed"
    )


    print(

        "Jobs saved:",

        len(jobs)

    )







if __name__ == "__main__":

    run_scrapers()