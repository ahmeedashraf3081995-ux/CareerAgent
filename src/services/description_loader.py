def load_descriptions(jobs):

    """
    MVP version:
    Descriptions are skipped.
    LinkedIn scraping only collects:
    title, company, location, url
    """

    for job in jobs:

        if "description" not in job:

            job["description"] = ""


    return jobs