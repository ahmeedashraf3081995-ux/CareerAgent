from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# AI Job Analysis
# ============================================================

def analyze_job_against_cv(
    cv_text,
    job
):

    title = job.get(
        "job_title",
        ""
    )

    company = job.get(
        "company",
        ""
    )

    description = job.get(
        "description",
        ""
    )

    score = job.get(
        "match_score",
        0
    )


    matched_skills = job.get(
        "matched_skills",
        []
    )


    missing_skills = job.get(
        "missing_skills",
        []
    )


    prompt = f"""
You are CareerAgent's career advisor.

Analyze this job specifically against the candidate's CV.

Do NOT invent experience.

The candidate should only be advised to claim a skill if the CV
actually supports it.

CV:
----------------
{cv_text}
----------------

JOB TITLE:
{title}

COMPANY:
{company}

JOB DESCRIPTION:
----------------
{description}
----------------

CURRENT MATCH SCORE:
{score}

CURRENT MATCHED SKILLS:
{matched_skills}

CURRENT MISSING SKILLS:
{missing_skills}

Provide:

1. A concise explanation of the role.
2. Why the candidate matches.
3. Genuine gaps.
4. CV improvement suggestions.
5. Application recommendation.
6. Specific keywords from the job description that are supported
   by the CV.
7. Keywords that should NOT be added because they are unsupported.

Return ONLY JSON:

{{
    "cv_job_brief": "",
    "why_you_match": [],
    "skill_gaps": [],
    "cv_suggestions": [],
    "supported_keywords": [],
    "unsupported_keywords": [],
    "application_recommendation": "",
    "recommendation_reason": ""
}}
"""


    system_prompt = """
You are CareerAgent's AI career advisor.

Never fabricate candidate experience.

Never recommend falsely claiming a skill.

Return valid JSON only.
"""


    try:

        response = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0.15,

            json_mode=True

        )


        data = extract_json(
            response
        )


    except Exception as e:

        print(
            "AI job analysis error:",
            e
        )

        data = {}


    job["cv_job_brief"] = data.get(

        "cv_job_brief",

        ""

    )


    job["why_you_match"] = data.get(

        "why_you_match",

        []

    )


    job["skill_gaps"] = data.get(

        "skill_gaps",

        []

    )


    job["cv_suggestions"] = data.get(

        "cv_suggestions",

        []

    )


    job["supported_keywords"] = data.get(

        "supported_keywords",

        []

    )


    job["unsupported_keywords"] = data.get(

        "unsupported_keywords",

        []

    )


    job["application_recommendation"] = data.get(

        "application_recommendation",

        ""

    )


    job["recommendation_reason"] = data.get(

        "recommendation_reason",

        ""

    )


    return job


# ============================================================
# Analyze Multiple Jobs
# ============================================================

def analyze_jobs_against_cv(
    cv_text,
    jobs
):

    results = []


    for job in jobs:

        try:

            analyzed = analyze_job_against_cv(

                cv_text,

                job

            )

            results.append(
                analyzed
            )

        except Exception as e:

            print(
                "Job analysis failed:",
                e
            )

            results.append(
                job
            )


    return results