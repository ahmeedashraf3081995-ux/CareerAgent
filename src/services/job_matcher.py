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
# Skill Formatting
# ==================================================

def format_skill(skill):

    if not skill:
        return ""


    skill = str(
        skill
    ).strip()


    special_cases = {

        "sap": "SAP",

        "erp": "ERP",

        "s&op": "S&OP",

        "ai": "AI",

        "ml": "ML",

        "sql": "SQL",

        "crm": "CRM",

        "kpi": "KPI",

        "kpis": "KPIs",

        "sku": "SKU",

        "skus": "SKUs",

        "otb": "OTB",

        "woc": "WOC",

        "mape": "MAPE",

        "bi": "BI",

        "power bi": "Power BI",

        "tableau": "Tableau",

        "python": "Python",

        "excel": "Excel",

        "oracle": "Oracle",

        "nielsen": "Nielsen",

        "looker studio": "Looker Studio"

    }


    lower_skill = skill.lower()


    if lower_skill in special_cases:

        return special_cases[
            lower_skill
        ]


    words = skill.split()


    formatted = []


    for word in words:

        lower_word = word.lower()


        if lower_word in special_cases:

            formatted.append(
                special_cases[
                    lower_word
                ]
            )

        else:

            formatted.append(
                word.capitalize()
            )


    return " ".join(
        formatted
    )


# ==================================================
# Format Skills
# ==================================================

def format_skills(skills):

    formatted = []


    for skill in skills:

        value = format_skill(
            skill
        )


        if value and value not in formatted:

            formatted.append(
                value
            )


    return formatted


# ==================================================
# Normalize Text
# ==================================================

def normalize(text):

    if not text:
        return ""


    return re.sub(
        r"[^a-zA-Z0-9&\s]",
        " ",
        str(text).lower()
    )


# ==================================================
# Extract Skills
# ==================================================

def extract_skills(text):

    text = normalize(
        text
    )

    found = []


    for skill in SKILLS:

        if skill in text:

            found.append(
                skill
            )


    return list(
        set(found)
    )


# ==================================================
# Experience Detection
# ==================================================

def extract_years(text):

    text = normalize(
        text
    )


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
# Experience Score
# ==================================================

def calculate_experience_score(
    cv_years,
    required_years
):

    # ------------------------------------------
    # No CV Experience Found
    # ------------------------------------------

    if cv_years <= 0:

        return 0


    # ------------------------------------------
    # Job Does Not Specify Experience
    # ------------------------------------------

    if required_years <= 0:

        return 85


    # ------------------------------------------
    # CV Meets Or Exceeds Requirement
    # ------------------------------------------

    if cv_years >= required_years:

        # Extra experience is positive,
        # but we don't reward it excessively.

        return 100


    # ------------------------------------------
    # Calculate Experience Ratio
    # ------------------------------------------

    ratio = (
        cv_years
        /
        required_years
    )


    # ------------------------------------------
    # Slightly Below Requirement
    # ------------------------------------------

    if ratio >= 0.80:

        return 90


    # ------------------------------------------
    # Moderately Below Requirement
    # ------------------------------------------

    if ratio >= 0.60:

        return 75


    # ------------------------------------------
    # Significantly Below Requirement
    # ------------------------------------------

    if ratio >= 0.40:

        return 55


    # ------------------------------------------
    # Very Significant Gap
    # ------------------------------------------

    return 35


# ==================================================
# Title Matching
# ==================================================

def calculate_title_score(
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


    return min(
        score,
        100
    )


# ==================================================
# Seniority Matching
# ==================================================

def seniority_score(
    cv_text,
    job_title
):

    cv = normalize(
        cv_text
    )

    title = normalize(
        job_title
    )


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


    return min(
        score,
        100
    )


# ==================================================
# Industry Match
# ==================================================

def industry_score(
    cv_text,
    job_text
):

    cv = normalize(
        cv_text
    )

    job = normalize(
        job_text
    )


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

def find_missing_skills(
    job_skills,
    cv_skills
):

    cv_skills_clean = set(

        skill.lower().strip()

        for skill in cv_skills

    )


    missing = []


    for skill in job_skills:

        skill_clean = (
            skill.lower().strip()
        )


        if skill_clean not in cv_skills_clean:

            formatted = format_skill(
                skill
            )


            if formatted:

                missing.append(
                    formatted
                )


    return missing[:10]


# ==================================================
# Explanation
# ==================================================

def create_reason(
    matched,
    score,
    cv_years,
    job_years
):

    formatted_matched = format_skills(
        matched
    )


    if score >= 85:

        reason = (
            "Excellent match. Your experience aligns "
            "well with this role"
        )


    elif score >= 70:

        reason = (
            "Good match. Your background has several "
            "relevant areas for this role"
        )


    else:

        reason = (
            "Partial match. Some relevant experience "
            "was identified, but there are areas that "
            "could be strengthened"
        )


    # ------------------------------------------
    # Skills
    # ------------------------------------------

    if formatted_matched:

        reason += (
            " through: "
            +
            ", ".join(
                formatted_matched[:6]
            )
        )


    # ------------------------------------------
    # Experience
    # ------------------------------------------

    if job_years:

        if cv_years >= job_years:

            reason += (
                f". Your CV shows approximately "
                f"{cv_years} years of experience, "
                f"meeting the {job_years}-year requirement"
            )

        elif cv_years:

            reason += (
                f". Your CV shows approximately "
                f"{cv_years} years of experience "
                f"versus the {job_years}-year requirement"
            )


    return reason + "."


# ==================================================
# Main Matching Function
# ==================================================

def match_jobs(
    cv_text,
    jobs
):

    # ==================================================
    # CV Analysis
    # ==================================================

    cv_skills = extract_skills(
        cv_text
    )


    cv_years = extract_years(
        cv_text
    )


    print(
        "CV experience detected:",
        cv_years,
        "years"
    )


    results = []


    # ==================================================
    # Match Every Job
    # ==================================================

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


        # ------------------------------------------
        # Job Skills
        # ------------------------------------------

        job_skills = extract_skills(
            job_text
        )


        # ------------------------------------------
        # Matching Skills
        # ------------------------------------------

        matched_skills = list(

            set(cv_skills)

            &

            set(job_skills)

        )


        matched_skills = format_skills(
            matched_skills
        )


        # ------------------------------------------
        # Skill Score
        # ------------------------------------------

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


        # ------------------------------------------
        # Title Score
        # ------------------------------------------

        title_score = calculate_title_score(

            cv_text,

            title

        )


        # ------------------------------------------
        # Seniority Score
        # ------------------------------------------

        senior_score = seniority_score(

            cv_text,

            title

        )


        # ------------------------------------------
        # Industry Score
        # ------------------------------------------

        industry = industry_score(

            cv_text,

            job_text

        )


        # ------------------------------------------
        # Experience
        # ------------------------------------------

        job_years = extract_years(
            job_text
        )


        experience_score = calculate_experience_score(

            cv_years,

            job_years

        )


        print(

            f"{title} | "

            f"CV Years: {cv_years} | "

            f"Required: {job_years} | "

            f"Experience Score: {experience_score}"

        )


        # ==================================================
        # Final Score
        # ==================================================

        final_score = round(

            (skill_score * 0.35)

            +

            (title_score * 0.20)

            +

            (senior_score * 0.10)

            +

            (industry * 0.10)

            +

            (experience_score * 0.25)

        )


        final_score = min(

            final_score,

            100

        )


        # ==================================================
        # Missing Skills
        # ==================================================

        missing_skills = find_missing_skills(

            job_skills,

            cv_skills

        )


        # ==================================================
        # Save Results
        # ==================================================

        job["match_score"] = final_score


        job["matched_skills"] = matched_skills


        job["missing_skills"] = missing_skills


        job["cv_years"] = cv_years


        job["required_years"] = job_years


        job["experience_score"] = experience_score


        job["match_reason"] = create_reason(

            matched_skills,

            final_score,

            cv_years,

            job_years

        )


        # ==================================================
        # Match Level
        # ==================================================

        if final_score >= 85:

            job["match_level"] = (
                "🔥 Excellent Match"
            )


        elif final_score >= 70:

            job["match_level"] = (
                "✅ Good Match"
            )


        elif final_score >= 50:

            job["match_level"] = (
                "⚠️ Partial Match"
            )


        else:

            job["match_level"] = (
                "❌ Weak Match"
            )


        results.append(
            job
        )


    # ==================================================
    # Highest Match First
    # ==================================================

    results.sort(

        key=lambda x: x.get(

            "match_score",

            0

        ),

        reverse=True

    )


    return results