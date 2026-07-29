import json
import os
from datetime import datetime


OUTPUT_FILE = "data/jobs/jobs_database.json"


# Target Dubai roles
TARGET_ROLES = [
    "Demand Planner",
    "Supply Planner",
    "Material Planner",
    "S&OP Planner",
    "Inventory Planner",
    "Replenishment Planner",
    "Planning Manager"
]


COMPANIES = [
    {
        "company": "Amazon",
        "url": "https://www.amazon.jobs",
        "jobs": [
            {
                "job_title": "Senior Demand Planner",
                "description":
                "Demand planning, forecasting, inventory optimization, S&OP, SAP, Excel, replenishment planning, MENA operations, 5+ years experience"
            }
        ]
    },

    {
        "company": "P&G",
        "url": "https://www.pgcareers.com",
        "jobs": [
            {
                "job_title": "Supply Planner",
                "description":
                "Supply planning, material planning, production planning, SAP, inventory management, forecasting, replenishment, S&OP"
            }
        ]
    },

    {
        "company": "Unilever",
        "url": "https://careers.unilever.com",
        "jobs": [
            {
                "job_title": "Material Planning Manager",
                "description":
                "Material planning, MRP, SAP, production planning, inventory optimization, supply chain planning, demand forecasting, supplier collaboration"
            }
        ]
    },

    {
        "company": "Samsung Electronics",
        "url": "https://www.samsung.com/careers/",
        "jobs": [
            {
                "job_title": "Demand & Supply Planning Manager",
                "description":
                "Demand planning, supply planning, forecasting, SAP, inventory management, sales planning, MENA operations, S&OP"
            }
        ]
    }
]


def build_database():

    jobs = []


    for company in COMPANIES:

        for job in company["jobs"]:

            jobs.append({

                "company":
                company["company"],

                "job_title":
                job["job_title"],

                "location":
                "Dubai, UAE",

                "url":
                company["url"],

                "description":
                job["description"],

                "target_roles":
                TARGET_ROLES,

                "scraped_date":
                str(datetime.now())

            })


    os.makedirs(
        "data/jobs",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            jobs,
            file,
            indent=2,
            ensure_ascii=False
        )


    print(
        f"Saved {len(jobs)} Dubai jobs"
    )

    print(
        OUTPUT_FILE
    )



if __name__ == "__main__":

    build_database()