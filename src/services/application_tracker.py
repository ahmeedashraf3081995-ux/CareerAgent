import json
import os
from datetime import datetime



FILE = "saved_jobs.json"





# ==================================================
# Load Jobs
# ==================================================

def load_jobs():

    if not os.path.exists(FILE):

        return []


    try:

        with open(

            FILE,

            "r",

            encoding="utf-8"

        ) as f:


            return json.load(f)


    except Exception:


        return []





# ==================================================
# Save Jobs
# ==================================================

def save_jobs(jobs):


    with open(

        FILE,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            jobs,

            f,

            indent=4,

            ensure_ascii=False

        )





# ==================================================
# Save New Job
# ==================================================

def save_job(job):


    jobs = load_jobs()



    job_id = (

        job.get(
            "url",
            ""

        )

        or

        (

            job.get(
                "job_title",
                ""

            )

            +

            job.get(
                "company",
                ""

            )

        )

    )



    # Check duplicates

    for existing in jobs:


        existing_id = (

            existing.get(
                "url",
                ""

            )

            or

            (

                existing.get(
                    "job_title",
                    ""

                )

                +

                existing.get(
                    "company",
                    ""

                )

            )

        )


        if existing_id == job_id:


            return False





    job["status"] = "❤️ Saved"


    job["saved_date"] = (

        datetime.now()

        .strftime(

            "%Y-%m-%d"

        )

    )


    jobs.append(
        job
    )


    save_jobs(
        jobs
    )


    return True





# ==================================================
# Update Status
# ==================================================

def update_job_status(

    job_identifier,

    status

):


    jobs = load_jobs()



    updated = False



    for job in jobs:



        current_id = (

            job.get(
                "url",
                ""

            )

            or

            (

                job.get(
                    "job_title",
                    ""

                )

                +

                job.get(
                    "company",
                    ""

                )

            )

        )



        if current_id == job_identifier:


            job["status"] = status


            job["last_update"] = (

                datetime.now()

                .strftime(

                    "%Y-%m-%d"

                )

            )


            updated = True




    if updated:


        save_jobs(
            jobs
        )



    return updated





# ==================================================
# Delete Job
# ==================================================

def delete_job(

    job_identifier

):


    jobs = load_jobs()



    remaining = []



    removed = False



    for job in jobs:



        current_id = (

            job.get(
                "url",
                ""

            )

            or

            (

                job.get(
                    "job_title",
                    ""

                )

                +

                job.get(
                    "company",
                    ""

                )

            )

        )



        if current_id == job_identifier:


            removed = True


        else:


            remaining.append(
                job
            )



    if removed:


        save_jobs(
            remaining
        )



    return removed