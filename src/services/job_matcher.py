from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# Helpers
# ============================================================

def safe_list(value):

    if isinstance(
        value,
        list
    ):

        return value

    return []


def safe_number(value):

    try:

        return int(
            float(value)
        )

    except Exception:

        return 0


# ============================================================
# AI Job Matching
# ============================================================

def match_jobs(
    cv_text,
    jobs
):

    if not jobs:

        return []


    results = []


    # ========================================================
    # Analyze Jobs
    # ========================================================

    for job in jobs:

        title = job.get(
            "job_title",
            ""
        )

        company = job.get(
            "company",
            ""
        )

        location = job.get(
            "location",
            ""
        )

        description = job.get(
            "description",
            ""
        )

        url = job.get(
            "url",
            ""
        )


        prompt = f"""
You are an expert recruiter and career matching engine.

Evaluate how well the candidate matches this job.

IMPORTANT:

Use ONLY evidence contained in the CV.

Do not assume the candidate has a skill simply because it is
common for the profession.

Do not invent experience.

Evaluate:

1. Overall match.
2. Skills match.
3. Job-title/function match.
4. Seniority match.
5. Industry match.
6. Experience match.
7. Missing or insufficiently demonstrated skills.
8. Strongest matching areas.
9. Main weaknesses.
10. Whether the candidate should apply.

CV:
----------------
{cv_text}
----------------

JOB TITLE:
{title}

COMPANY:
{company}

LOCATION:
{location}

JOB DESCRIPTION:
----------------
{description}
----------------

Return ONLY JSON:

{{
    "match_score": 0,
    "skill_score": 0,
    "title_score": 0,
    "seniority_score": 0,
    "industry_score": 0,
    "experience_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "required_years": 0,
    "candidate_years": 0,
    "should_apply": true,
    "match_level": "",
    "match_reason": ""
}}

Scoring guidance:

90-100 = Exceptional match
80-89 = Excellent match
70-79 = Good match
60-69 = Moderate match
50-59 = Partial match
Below 50 = Weak match

Be realistic.

Do not inflate the score simply because the candidate has a
similar job title.
"""


        system_prompt = """
You are CareerAgent's AI job matching engine.

You are an objective recruiter.

Accuracy is more important than generosity.

Never fabricate candidate experience.

Return valid JSON only.
"""


        try:

            response = ask_ollama(

                prompt,

                system_prompt=system_prompt,

                temperature=0.1,

                json_mode=True

            )


            data = extract_json(
                response
            )


        except Exception as e:

            print(
                "AI matching error:",
                e
            )

            data = {}


        # ====================================================
        # Save AI Results
        # ====================================================

        job["match_score"] = min(

            max(

                safe_number(
                    data.get(
                        "match_score",
                        0
                    )
                ),

                0

            ),

            100

        )


        job["skill_score"] = safe_number(
            data.get(
                "skill_score",
                0
            )
        )


        job["title_score"] = safe_number(
            data.get(
                "title_score",
                0
            )
        )


        job["seniority_score"] = safe_number(
            data.get(
                "seniority_score",
                0
            )
        )


        job["industry_score"] = safe_number(
            data.get(
                "industry_score",
                0
            )
        )


        job["experience_score"] = safe_number(
            data.get(
                "experience_score",
                0
            )
        )


        job["matched_skills"] = safe_list(
            data.get(
                "matched_skills",
                []
            )
        )


        job["missing_skills"] = safe_list(
            data.get(
                "missing_skills",
                []
            )
        )


        job["strengths"] = safe_list(
            data.get(
                "strengths",
                []
            )
        )


        job["weaknesses"] = safe_list(
            data.get(
                "weaknesses",
                []
            )
        )


        job["required_years"] = safe_number(
            data.get(
                "required_years",
                0
            )
        )


        job["cv_years"] = safe_number(
            data.get(
                "candidate_years",
                0
            )
        )


        job["should_apply"] = bool(
            data.get(
                "should_apply",
                False
            )
        )


        job["match_level"] = data.get(

            "match_level",

            "Unknown"

        )


        job["match_reason"] = data.get(

            "match_reason",

            ""

        )


        results.append(
            job
        )


    # ========================================================
    # Highest Match First
    # ========================================================

    results.sort(

        key=lambda x: x.get(
            "match_score",
            0
        ),

        reverse=True

    )


    return results