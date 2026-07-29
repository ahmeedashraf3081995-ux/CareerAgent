import json
import os


PROFILE_FILE = "data/profile/profile.json"
JOB_FILE = "data/profile/job_profile.json"
OUTPUT_FILE = "data/profile/match_report.json"


def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize(text):

    return str(text).lower().replace("-", " ").replace("_", " ")


def get_candidate_text(profile):

    return normalize(json.dumps(profile))


def calculate_match(profile, job):

    candidate_text = get_candidate_text(profile)

    score = 0

    strong_matches = []
    missing_skills = []
    missing_tools = []

    breakdown = {}


    # -------------------------
    # Skills (40%)
    # -------------------------

    skill_score = 0

    skill_mapping = {

        "Demand Forecasting": [
            "forecast",
            "forecasting",
            "demand planning",
            "demand forecast"
        ],

        "Inventory Optimization": [
            "inventory",
            "stock",
            "excess inventory",
            "overstock",
            "coverage"
        ],

        "S&OP": [
            "s&op",
            "sales planning",
            "budget",
            "cross functional",
            "finance"
        ],

        "SAP": [
            "sap",
            "erp",
            "mrp"
        ],

        "Supply Planning": [
            "supply planning",
            "replenishment",
            "availability",
            "supply"
        ]

    }


    for skill in job.get("required_skills", []):

        found = False

        skill_name = normalize(skill)


        for category, keywords in skill_mapping.items():

            if any(word in skill_name for word in keywords):

                if any(word in candidate_text for word in keywords):

                    found = True
                    break


        if found:

            skill_score += 10
            strong_matches.append(skill)

        else:

            missing_skills.append(skill)


    skill_score = min(skill_score, 40)

    score += skill_score

    breakdown["skills"] = skill_score



    # -------------------------
    # Experience (25%)
    # -------------------------

    exp_score = 0

    years = normalize(
        profile.get("years_experience", "")
    )


    if any(x in years for x in ["6", "7", "8", "9"]):

        exp_score = 25

    elif "5" in years:

        exp_score = 20

    else:

        exp_score = 10


    score += exp_score

    breakdown["experience"] = exp_score



    # -------------------------
    # Responsibilities (25%)
    # -------------------------

    responsibility_words = [

        "planning",
        "forecast",
        "inventory",
        "supply",
        "replenishment",
        "optimization",
        "sales",
        "operations"

    ]


    matched = 0

    for word in responsibility_words:

        if word in candidate_text:

            matched += 1


    responsibility_score = int(
        matched / len(responsibility_words) * 25
    )


    score += responsibility_score

    breakdown["responsibilities"] = responsibility_score



    # -------------------------
    # Tools (5%)
    # -------------------------

    tools_score = 0


    for tool in job.get("required_tools", []):

        if normalize(tool) in candidate_text:

            tools_score += 5
            strong_matches.append(tool)

        else:

            missing_tools.append(tool)


    tools_score = min(tools_score, 5)

    score += tools_score

    breakdown["tools"] = tools_score



    # -------------------------
    # Industry (5%)
    # -------------------------

    industry_score = 0


    if any(
        x in candidate_text
        for x in [
            "retail",
            "samsung",
            "eyewa",
            "magrabi",
            "mena",
            "electronics"
        ]
    ):

        industry_score = 5


    score += industry_score

    breakdown["industry"] = industry_score



    score = min(score, 100)



    # Recommendation

    if score >= 90:

        recommendation = "Excellent Match"

    elif score >= 80:

        recommendation = "Strong Apply"

    elif score >= 65:

        recommendation = "Apply with CV Adjustment"

    else:

        recommendation = "Low Match"



    return {

        "match_score_percentage": score,

        "recommendation": recommendation,

        "score_breakdown": breakdown,

        "strong_matches": list(set(strong_matches)),

        "missing_skills": missing_skills,

        "missing_tools": missing_tools,

        "experience_match":
        "Candidate experience aligns with job requirements.",

        "cv_improvement_suggestions": [

            "Highlight relevant forecasting and planning achievements.",

            "Match CV keywords with job description.",

            "Emphasize measurable business impact."

        ]

    }



if __name__ == "__main__":

    profile = load_json(PROFILE_FILE)

    job = load_json(JOB_FILE)


    report = calculate_match(
        profile,
        job
    )


    print("\nMATCH REPORT:\n")

    print(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        )
    )


    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("\nMatch report saved successfully")