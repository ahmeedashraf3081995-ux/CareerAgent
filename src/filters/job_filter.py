import json
import os


JOBS_FILE = "data/jobs/jobs_database.json"
OUTPUT_FILE = "data/jobs/filtered_jobs.json"


def load_jobs():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_jobs(jobs):

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



def normalize(text):

    return text.lower().strip()



def filter_jobs(
        jobs,
        locations=None,
        keywords=None
):

    filtered = []


    for job in jobs:

        job_title = normalize(
            job.get("job_title", "")
        )

        description = normalize(
            job.get("description", "")
        )

        location = normalize(
            job.get("location", "")
        )


        location_found = True


        if locations:

            location_found = False

            for loc in locations:

                if normalize(loc) in location:

                    location_found = True
                    break



        keyword_found = True


        if keywords:

            keyword_found = False

            for keyword in keywords:

                keyword = normalize(keyword)


                if (
                    keyword in job_title
                    or keyword in description
                ):

                    keyword_found = True
                    break



        if location_found and keyword_found:

            filtered.append(job)



    return filtered



if __name__ == "__main__":


    print("Job Filter Engine\n")


    jobs = load_jobs()



    # TEST FILTERS
    # Later dashboard will replace these


    selected_locations = [
        "US",
        "GB",
        "FR",
        "LU"
    ]


    selected_keywords = [
        "Demand Planner",
        "Supply Planner",
        "Material Planner",
        "Planning",
        "S&OP"
    ]



    results = filter_jobs(
        jobs,
        selected_locations,
        selected_keywords
    )



    save_jobs(results)



    print("Filtering completed")

    print(
        "Jobs found:",
        len(results)
    )

    print(
        "Saved:",
        OUTPUT_FILE
    )


    print("\nResults:")


    for job in results:

        print(
            "-",
            job.get("company"),
            "|",
            job.get("job_title"),
            "|",
            job.get("location")
        )