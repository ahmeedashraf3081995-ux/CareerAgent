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

    return skill.strip()


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

    matched_skills = job.get(
        "matched_skills",
        []
    )

    missing_skills = job.get(
        "missing_skills",
        []
    )

    score = job.get(
        "match_score",
        0
    )


    # ------------------------------------------
    # Basic job information
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
    # Matched skills
    # ------------------------------------------

    matched = [
        format_skill(skill)
        for skill in matched_skills
        if skill
    ]


    missing = [
        format_skill(skill)
        for skill in missing_skills
        if skill
    ]


    # ------------------------------------------
    # Build brief
    # ------------------------------------------

    parts = []


    if title and company:

        parts.append(
            f"This {title} role at {company} focuses on "
            f"responsibilities and requirements outlined in "
            f"the job description."
        )

    elif title:

        parts.append(
            f"This {title} role focuses on the responsibilities "
            f"and requirements outlined in the job description."
        )


    if matched:

        matched_text = ", ".join(
            matched[:5]
        )

        parts.append(
            f"Your CV aligns particularly well with "
            f"{matched_text}."
        )


    if missing:

        missing_text = ", ".join(
            missing[:4]
        )

        parts.append(
            f"The main areas to strengthen for this role are "
            f"{missing_text}."
        )


    if score >= 85:

        parts.append(
            "Overall, this appears to be a strong opportunity "
            "based on your current CV."
        )

    elif score >= 70:

        parts.append(
            "Overall, this appears to be a good opportunity "
            "with some areas that could be strengthened."
        )

    else:

        parts.append(
            "Overall, the role has some relevant elements, "
            "but your CV may need stronger alignment before applying."
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


    missing_skills = job.get(
        "missing_skills",
        []
    )


    matched_skills = job.get(
        "matched_skills",
        []
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
                f"in your CV."
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
            f"{matched_text}, as these areas already align "
            f"well with the role."
        )


    # ------------------------------------------
    # Description-based suggestions
    # ------------------------------------------

    description_lower = description.lower()


    keyword_groups = [

        (
            "forecasting",
            "Highlight specific forecasting methods, "
            "forecast accuracy improvements, or forecasting "
            "responsibilities."
        ),

        (
            "inventory",
            "Highlight measurable inventory optimization, "
            "stock availability, WOC, safety stock, or "
            "inventory reduction achievements."
        ),

        (
            "s&op",
            "If you have S&OP experience, make your involvement "
            "and cross-functional responsibilities explicit."
        ),

        (
            "sales and operations planning",
            "If applicable, clearly mention your Sales and "
            "Operations Planning experience."
        ),

        (
            "power bi",
            "Highlight specific Power BI dashboards, reports, "
            "or planning decisions supported by your analysis."
        ),

        (
            "tableau",
            "Highlight relevant Tableau reporting or dashboard "
            "development experience."
        ),

        (
            "sap",
            "Make your SAP experience more visible and mention "
            "the planning processes or transactions you managed."
        ),

        (
            "excel",
            "Highlight advanced Excel capabilities and quantify "
            "how they improved planning or reporting."
        ),

        (
            "automation",
            "If applicable, highlight automation projects and "
            "the time or effort saved."
        ),

        (
            "stakeholder",
            "Emphasize cross-functional stakeholder management "
            "and collaboration."
        )

    ]


    for keyword, suggestion in keyword_groups:

        if keyword in description_lower:

            # Avoid excessive suggestions
            if suggestion not in suggestions:

                suggestions.append(
                    suggestion
                )


    # ------------------------------------------
    # Low Score
    # ------------------------------------------

    if score < 70:

        suggestions.append(
            "Review the role requirements carefully and "
            "prioritize the most relevant experience in your "
            "CV before applying."
        )


    # ------------------------------------------
    # Strong Score
    # ------------------------------------------

    elif score >= 85:

        suggestions.append(
            "Your CV already shows strong alignment with this "
            "role, so focus on making your strongest relevant "
            "achievements easy to find."
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

    job["cv_job_brief"] = create_cv_job_brief(
        cv_text,
        job
    )


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