import re





# Titles that are relevant for planning / supply chain careers

TARGET_KEYWORDS = [

    "planner",

    "planning",

    "demand",

    "supply",

    "inventory",

    "s&op",

    "forecast",

    "merchandise",

    "supply chain",

    "operations",

    "procurement"

]





def normalize(text):

    return re.sub(

        r"[^a-zA-Z0-9\s&]",

        " ",

        text.lower()

    )





def calculate_title_relevance(

    cv_text,

    job_title

):


    cv = normalize(
        cv_text
    )


    title = normalize(
        job_title
    )


    score = 0



    for keyword in TARGET_KEYWORDS:


        if keyword in cv and keyword in title:


            score += 10



        elif keyword in title:


            score += 5



    return score





def pre_filter_jobs(

    cv_text,

    jobs,

    limit=100

):


    scored_jobs = []



    for job in jobs:


        title = job.get(

            "job_title",

            ""

        )


        score = calculate_title_relevance(

            cv_text,

            title

        )


        job["title_relevance"] = score



        scored_jobs.append(
            job
        )




    scored_jobs.sort(

        key=lambda x:

        x.get(

            "title_relevance",

            0

        ),

        reverse=True

    )



    return scored_jobs[:limit]