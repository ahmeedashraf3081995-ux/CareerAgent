import json
import os


INPUT_FILE = "output/job_ranking.json"

OUTPUT_FILE = "output/enhanced_job_ranking.json"



def explain_job(job):


    areas = job.get(
        "matched_areas",
        []
    )


    score = job.get(
        "match_score",
        0
    )


    explanation = {}



    # Match explanation

    if score >= 80:

        explanation["match_reason"] = (
            "Strong match because your experience directly "
            "covers the core responsibilities of this role."
        )

    elif score >= 50:

        explanation["match_reason"] = (
            "Good match. Some experience aligns, "
            "but additional positioning is required."
        )

    else:

        explanation["match_reason"] = (
            "Partial match. Consider only if the role "
            "offers career growth."
        )



    # Skills found

    explanation["your_strengths"] = areas



    # Missing skills detection

    common_missing = [

        "SQL",

        "Python",

        "Advanced Power BI",

        "Machine Learning",

        "SAP IBP"

    ]


    missing=[]


    for skill in common_missing:


        if skill.lower() not in str(areas).lower():

            missing.append(skill)



    explanation["potential_gaps"] = missing[:3]



    # Interview preparation

    explanation["interview_focus"] = [

        "Forecast accuracy improvement",

        "Inventory optimization",

        "S&OP process",

        "Stakeholder management"

    ]



    # CV keywords

    explanation["cv_keywords"] = areas



    job["ai_explanation"] = explanation


    return job





def run():

    print(
        "AI Job Explanation Engine"
    )


    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        jobs=json.load(f)



    enhanced=[]


    for job in jobs:

        enhanced.append(
            explain_job(job)
        )



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            enhanced,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        "Completed"
    )

    print(
        "Jobs enhanced:",
        len(enhanced)
    )



if __name__ == "__main__":

    run()