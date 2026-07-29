import json
import os
import sys

sys.path.append(
    os.path.dirname(__file__)
)

from amazon_scraper import scrape_amazon


OUTPUT = "data/jobs/jobs_database.json"


def save_jobs(jobs):

    os.makedirs(
        "data/jobs",
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            jobs,
            file,
            indent=2,
            ensure_ascii=False
        )


def run_scrapers():

    print("Starting Real Job Scraper...\n")

    all_jobs = []


    amazon_jobs = scrape_amazon()

    all_jobs.extend(
        amazon_jobs
    )


    save_jobs(
        all_jobs
    )


    print(
        "\nScraping completed"
    )

    print(
        "Jobs collected:",
        len(all_jobs)
    )


if __name__ == "__main__":

    run_scrapers()