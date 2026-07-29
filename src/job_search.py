import json
from job_matcher import job_matcher
from report_generator import generate_report


def load_jobs():

    with open(
        "data/jobs/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def rank_jobs():

    jobs = load_jobs()

    results = []

    for job in jobs:

        result = job_matcher(job)

        results.append({
            "job": job,
            "result": result
        })

    results.sort(
        key=lambda x: x["result"]["overall_score"],
        reverse=True
    )

    return results


if __name__ == "__main__":

    ranked_jobs = rank_jobs()

    for item in ranked_jobs:

        generate_report(
            item["job"],
            item["result"]
        )