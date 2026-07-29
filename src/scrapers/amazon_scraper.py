import requests
from datetime import datetime


def scrape_amazon():

    jobs = []

    url = "https://www.amazon.jobs/en/search.json"

    params = {
        "base_query": "demand planner",
        "loc_query": "Dubai"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        data = response.json()


        for job in data.get("jobs", []):

            jobs.append({

                "company": "Amazon",

                "job_title":
                job.get("title"),

                "location":
                job.get("location"),

                "url":
                "https://www.amazon.jobs"
                + job.get("job_path"),

                "description":
                job.get("description",""),

                "scraped_date":
                str(datetime.now()),

                "source":
                "Amazon Careers API"

            })


    except Exception as e:

        print(
            "Amazon API error:",
            e
        )


    return jobs