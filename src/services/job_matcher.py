import re


# ==================================================
# Skill Database
# ==================================================

SKILLS = [

    # Planning
    "demand planning",
    "supply planning",
    "forecasting",
    "forecast",
    "statistical forecasting",
    "inventory management",
    "inventory optimization",
    "safety stock",
    "replenishment",
    "s&op",
    "sales and operations planning",
    "otb",
    "merchandise planning",
    "assortment planning",

    # Systems
    "sap",
    "oracle",
    "erp",

    # Analytics
    "excel",
    "advanced excel",
    "power bi",
    "tableau",
    "sql",
    "python",
    "analytics",
    "dashboard",
    "automation",

    # Supply Chain
    "vendor management",
    "procurement",
    "logistics",
    "warehouse",
    "transportation",

    # Business
    "retail",
    "e-commerce",
    "category management",
    "fmcg",
    "consumer goods"

]



# ==================================================
# Normalize Text
# ==================================================

def normalize(text):

    if not text:
        return ""


    return re.sub(
        r"[^a-zA-Z0-9&\s]",
        " ",
        text.lower()
    )



# ==================================================
# Extract Skills
# ==================================================

def extract_skills(text):

    text = normalize(text)

    found = []


    for skill in SKILLS:

        if skill in text:

            found.append(skill)


    return list(set(found))



# ==================================================
# Experience Detection
# ==================================================

def extract_years(text):

    text = normalize(text)


    matches = re.findall(
        r"(\d+)\+?\s*(?:years|year)",
        text
    )


    if matches:

        return max(
            int(x)
            for x in matches
        )


    return 0



# ==================================================
# Title Matching
# ==================================================

def calculate_title_score(cv_text, job_title):

    cv = normalize(cv_text)

    title = normalize(job_title)


    score = 0


    important_words = [

        "planner",
        "planning",
        "demand",
        "supply",
        "inventory",
        "forecast",
        "s&op",
        "merchandise",
        "analyst",
        "manager"

    ]


    for word in important_words:

        if word in cv and word in title:

            score += 15


    return min(score, 100)



# ==================================================
# Seniority Matching
# ==================================================

def seniority_score(cv_text, job_title):

    cv = normalize(cv_text)

    title = normalize(job_title)


    score = 50


    senior_words = [

        "senior",
        "lead",
        "manager",
        "head",
        "director"

    ]


    for word in senior_words:

        if word in cv and word in title:

            score += 10


    return min(score, 100)



# ==================================================
# Industry Match
# ==================================================

def industry_score(cv_text, job_text):

    cv = normalize(cv_text)

    job = normalize(job_text)


    industries = [

        "retail",
        "fmcg",
        "consumer goods",
        "e commerce",
        "electronics"

    ]


    for item in industries:

        if item in cv and item in job:

            return 100


    return 50



# ==================================================
# Missing Skills
# ==================================================

def find_missing_skills(job_skills, cv_skills):

    cv_skills_clean = set(

        skill.lower().strip()

        for skill in cv_skills

    )


    missing = []


    for skill in job_skills:

        skill_clean = skill.lower().strip()


        if skill_clean not in cv_skills_clean:

            missing.append(skill)


    return missing[:10]



# ==================================================
# Explanation
# ==================================================

def create_reason(matched, score):


    if score >= 85:

        return (

            "Excellent match. Your experience aligns with this role through: "

            +

            ", ".join(matched[:6])

        )


    elif score >= 70:

        return (

            "Good match. Relevant experience found in: "

            +

            ", ".join(matched[:6])

        )


    else:

        return (

            "Partial match. Consider improving your CV keywords and experience alignment."

        )



# ==================================================
# Main Matching Function
# ==================================================

def match_jobs(cv_text, jobs):


    cv_skills = extract_skills(cv_text)

    cv_years = extract_years(cv_text)


    results = []



    for job in jobs:


        title = job.get(
            "job_title",
            ""
        )


        description = job.get(
            "description",
            ""
        )


        job_text = (

            title

            +

            " "

            +

            description

        )



        job_skills = extract_skills(job_text)



        matched_skills = list(

            set(cv_skills)

            &

            set(job_skills)

        )



        # Skill Score

        skill_score = 0


        if job_skills:

            skill_score = round(

                (

                    len(matched_skills)

                    /

                    len(job_skills)

                )

                *

                100

            )



        title_score = calculate_title_score(

            cv_text,

            title

        )


        senior_score = seniority_score(

            cv_text,

            title

        )


        industry = industry_score(

            cv_text,

            job_text

        )



        job_years = extract_years(job_text)


        experience_score = 50



        if job_years and cv_years:


            if cv_years >= job_years:

                experience_score = 100

            else:

                experience_score = 70


        elif cv_years:

            experience_score = 80



        # Final Score

        final_score = round(

            (skill_score * 0.35)

            +

            (title_score * 0.25)

            +

            (senior_score * 0.15)

            +

            (industry * 0.10)

            +

            (experience_score * 0.15)

        )


        final_score = min(

            final_score,

            100

        )



        # Save Results

        job["match_score"] = final_score


        job["matched_skills"] = matched_skills


        job["missing_skills"] = find_missing_skills(

            job_skills,

            cv_skills

        )


        job["match_reason"] = create_reason(

            matched_skills,

            final_score

        )



        if final_score >= 85:

            job["match_level"] = "🔥 Excellent Match"


        elif final_score >= 70:

            job["match_level"] = "✅ Good Match"


        elif final_score >= 50:

            job["match_level"] = "⚠️ Partial Match"


        else:

            job["match_level"] = "❌ Weak Match"



        results.append(job)



    # Highest match first

    results.sort(

        key=lambda x: x.get(

            "match_score",

            0

        ),

        reverse=True

    )


    return results