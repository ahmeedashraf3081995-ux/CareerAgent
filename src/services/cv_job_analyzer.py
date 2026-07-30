import re


# ==================================================
# Helpers
# ==================================================

def clean_text(text):

    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip()


def format_skill(skill):

    if not skill:
        return ""

    skill = clean_text(skill)

    # Consistent UI capitalization
    words = skill.split()

    formatted_words = []

    special_cases = {
        "sap": "SAP",
        "erp": "ERP",
        "s&op": "S&OP",
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
        "looker studio": "Looker Studio",
    }

    lower_skill = skill.lower()

    if lower_skill in special_cases:
        return special_cases[lower_skill]

    for word in words:

        lower_word = word.lower()

        if lower_word in special_cases:
            formatted_words.append(
                special_cases[lower_word]
            )

        else:
            formatted_words.append(
                word.capitalize()
            )

    return " ".join(formatted_words)


def format_skills(skills):

    if not skills:
        return []

    formatted = []

    for skill in skills:

        formatted_skill = format_skill(
            skill
        )

        if (
            formatted_skill
            and formatted_skill not in formatted
        ):
            formatted.append(
                formatted_skill
            )

    return formatted


# ==================================================
# CV-Based Job Brief
# ==================================================

def create_cv_job_brief(
    cv_text,
    job
):

    title = clean_text(
        job.get(
            "job_title",
            ""
        )
    )

    company = clean_text(
        job.get(
            "company",
            ""
        )
    )

    description = clean_text(
        job.get(
            "description",
            ""
        )
    )

    matched_skills = format_skills(
        job.get(
            "matched_skills",
            []
        )
    )

    missing_skills = format_skills(
        job.get(
            "missing_skills",
            []
        )
    )

    score = job.get(
        "match_score",
        0
    )


    # ------------------------------------------
    # No Description Available
    # ------------------------------------------

    if not description:

        if score >= 85:

            return (
                f"This {title} role at {company} appears to be "
                f"a strong match for your background, with a "
                f"current match score of {score}%."
            )

        elif score >= 70:

            return (
                f"This {title} role at {company} appears relevant "
                f"to your background, with a current match score "
                f"of {score}%."
            )

        else:

            return (
                f"This {title} role at {company} has some "
                f"relevance to your background, with a current "
                f"match score of {score}%."
            )


    # ------------------------------------------
    # Build Brief
    # ------------------------------------------

    parts = []


    if title and company:

        parts.append(
            f"This {title} role at {company} is focused on "
            f"the responsibilities and requirements outlined "
            f"in the job description."
        )

    elif title:

        parts.append(
            f"This {title} role is focused on the "
            f"responsibilities and requirements outlined "
            f"in the job description."
        )


    # ------------------------------------------
    # Matching Skills
    # ------------------------------------------

    if matched_skills:

        matched_text = ", ".join(
            matched_skills[:5]
        )

        parts.append(
            f"Your CV aligns particularly well with "
            f"{matched_text}."
        )


    # ------------------------------------------
    # Missing Skills
    # ------------------------------------------

    if missing_skills:

        missing_text = ", ".join(
            missing_skills[:4]
        )

        parts.append(
            f"The main areas to strengthen for this role "
            f"are {missing_text}."
        )


    # ------------------------------------------
    # Overall Assessment
    # ------------------------------------------

    if score >= 85:

        parts.append(
            "Overall, this appears to be a strong opportunity "
            "based on the current alignment between your CV "
            "and the role."
        )

    elif score >= 70:

        parts.append(
            "Overall, this appears to be a good opportunity "
            "with a few areas that could be strengthened."
        )

    else:

        parts.append(
            "Overall, the role has some relevant elements, "
            "but your CV may need stronger alignment before "
            "applying."
        )


    return " ".join(parts)


# ==================================================
# CV Improvement Suggestions
# ==================================================

def create_cv_suggestions(
    cv_text,
    job
):

    suggestions = []


    missing_skills = format_skills(
        job.get(
            "missing_skills",
            []
        )
    )


    matched_skills = format_skills(
        job.get(
            "matched_skills",
            []
        )
    )


    description = clean_text(
        job.get(
            "description",
            ""
        )
    )


    score = job.get(
        "match_score",
        0
    )


    # ------------------------------------------
    # Missing Skills
    # ------------------------------------------

    for skill in missing_skills[:5]:

        if skill:

            suggestions.append(
                f"If you have relevant experience with "
                f"{skill}, consider making it more visible "
                f"in your CV by adding a specific achievement "
                f"or responsibility."
            )


    # ------------------------------------------
    # Matched Skills
    # ------------------------------------------

    if matched_skills:

        matched_text = ", ".join(
            matched_skills[:4]
        )

        suggestions.append(
            f"Emphasize your experience with "
            f"{matched_text}, particularly where you can "
            f"show measurable business impact."
        )


    # ------------------------------------------
    # Description-Based Suggestions
    # ------------------------------------------

    description_lower = (
        description.lower()
    )


    keyword_groups = [

        (
            "forecasting",
            "Highlight specific forecasting methods, "
            "forecast accuracy improvements, and measurable "
            "forecasting results."
        ),

        (
            "inventory",
            "Highlight measurable inventory optimization, "
            "stock availability, WOC, safety stock, or "
            "inventory reduction achievements."
        ),

        (
            "s&op",
            "If you have S&OP experience, clearly show your "
            "role in the process and your cross-functional "
            "involvement."
        ),

        (
            "sales and operations planning",
            "If applicable, clearly mention your Sales and "
            "Operations Planning experience and the business "
            "impact you delivered."
        ),

        (
            "power bi",
            "Highlight specific Power BI dashboards, reports, "
            "or planning decisions supported by your analysis."
        ),

        (
            "tableau",
            "Highlight relevant Tableau reporting, dashboard "
            "development, and business insights."
        ),

        (
            "sap",
            "Make your SAP experience more visible and mention "
            "the planning processes or transactions you managed."
        ),

        (
            "excel",
            "Highlight advanced Excel capabilities and quantify "
            "how they improved planning, analysis, or reporting."
        ),

        (
            "automation",
            "If applicable, highlight automation projects and "
            "quantify the time, effort, or error reduction achieved."
        ),

        (
            "stakeholder",
            "Emphasize cross-functional stakeholder management "
            "and collaboration with measurable outcomes where possible."
        ),

        (
            "leadership",
            "Highlight examples where you led initiatives, "
            "projects, or cross-functional activities."
        ),

        (
            "analytics",
            "Highlight analytical projects where your insights "
            "directly supported business or planning decisions."
        )

    ]


    for keyword, suggestion in keyword_groups:

        if keyword in description_lower:

            if suggestion not in suggestions:

                suggestions.append(
                    suggestion
                )


    # ------------------------------------------
    # Low Score
    # ------------------------------------------

    if score < 70:

        suggestions.append(
            "Review the key requirements of the role and "
            "prioritize the most relevant experience and "
            "achievements in your CV before applying."
        )


    # ------------------------------------------
    # Strong Score
    # ------------------------------------------

    elif score >= 85:

        suggestions.append(
            "Your CV already shows strong alignment with this "
            "role. Focus on making your strongest relevant "
            "achievements easy to identify."
        )


    # ------------------------------------------
    # Medium Score
    # ------------------------------------------

    elif score >= 70:

        suggestions.append(
            "Consider tailoring the wording of your strongest "
            "experience to reflect the terminology used in "
            "the job description."
        )


    # ------------------------------------------
    # Fallback
    # ------------------------------------------

    if not suggestions:

        suggestions.append(
            "Review the job description for role-specific "
            "keywords and make sure your most relevant "
            "achievements are clearly highlighted."
        )


    return suggestions[:8]


# ==================================================
# Analyze Job Against CV
# ==================================================

def analyze_job_against_cv(
    cv_text,
    job
):

    # ------------------------------------------
    # Format Skills For UI
    # ------------------------------------------

    job["matched_skills"] = format_skills(
        job.get(
            "matched_skills",
            []
        )
    )


    job["missing_skills"] = format_skills(
        job.get(
            "missing_skills",
            []
        )
    )


    # ------------------------------------------
    # Generate CV Job Brief
    # ------------------------------------------

    job["cv_job_brief"] = create_cv_job_brief(
        cv_text,
        job
    )


    # ------------------------------------------
    # Generate CV Suggestions
    # ------------------------------------------

    job["cv_suggestions"] = create_cv_suggestions(
        cv_text,
        job
    )


    return job


# ==================================================
# Analyze Multiple Jobs
# ==================================================

def analyze_jobs_against_cv(
    cv_text,
    jobs
):

    for job in jobs:

        analyze_job_against_cv(
            cv_text,
            job
        )


    return jobs