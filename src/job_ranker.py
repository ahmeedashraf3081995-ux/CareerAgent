import json
import os


INPUT_FILE = "data/jobs/jobs_database.json"
OUTPUT_FILE = "output/job_ranking.json"



# High importance
ROLE_KEYWORDS = {

    "demand planning":15,
    "supply planning":15,
    "material planning":15,
    "inventory planning":10,
    "inventory optimization":10,
    "forecasting":10,
    "s&op":10,
    "planning manager":15,
    "merchandise planning":10

}



# Technical skills
TECH_KEYWORDS = {

    "sap":5,
    "mrp":5,
    "excel":5,
    "power bi":5,
    "tableau":5

}



LEVEL_KEYWORDS = {

    "manager":10,
    "senior":8,
    "lead":8,
    "specialist":5

}



LOCATION_KEYWORDS = {

    "dubai":10,
    "uae":10,
    "mena":10,
    "middle east":10

}




def calculate_score(job):


    title = job.get(
        "job_title",
        ""
    ).lower()


    description = job.get(
        "description",
        ""
    ).lower()


    location = job.get(
        "location",
        ""
    ).lower()



    text = (
        title
        +
        " "
        +
        description
    )


    score = 0

    matched=[]



    # Roles

    for key,value in ROLE_KEYWORDS.items():

        if key in text:

            score += value

            matched.append(
                key.title()
            )



    # Technical

    for key,value in TECH_KEYWORDS.items():

        if key in text:

            score += value

            matched.append(
                key.upper()
            )



    # Seniority

    for key,value in LEVEL_KEYWORDS.items():

        if key in title:

            score += value

            matched.append(
                key.title()+" Level"
            )



    # Location

    for key,value in LOCATION_KEYWORDS.items():

        if key in location or key in text:

            score += value

            matched.append(
                key.upper()
            )



    if score > 100:

        score = 100



    if score >=85:

        recommendation="Excellent Match"

    elif score >=65:

        recommendation="Apply"

    else:

        recommendation="Review"



    return {

        "company":job.get("company"),

        "job_title":job.get("job_title"),

        "location":job.get("location"),

        "url":job.get("url"),

        "description":job.get("description"),

        "match_score":score,

        "recommendation":recommendation,

        "matched_areas":matched

    }




def main():


    with open(
        INPUT_FILE,
        encoding="utf-8"
    ) as f:

        jobs=json.load(f)



    results=[]


    for job in jobs:

        results.append(
            calculate_score(job)
        )



    results.sort(
        key=lambda x:x["match_score"],
        reverse=True
    )



    os.makedirs(
        "output",
        exist_ok=True
    )



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )



    print("Ranking completed")
    print("Jobs ranked:",len(results))



if __name__=="__main__":

    main()