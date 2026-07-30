import json

from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# Helpers
# ============================================================

def safe_list(value):

    if isinstance(value, list):
        return value

    return []


def safe_int(value, default=0):

    try:
        return int(float(value))
    except Exception:
        return default


def clean_score(value):

    score = safe_int(value)

    return max(
        0,
        min(100, score)
    )


# ============================================================
# AI Job Analysis
# ============================================================

def analyze_job_with_ai(
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

    location = job.get(
        "location",
        ""
    )

    description = job.get(
        "description",
        ""
    )


    prompt = f"""
You are CareerAgent's expert recruitment and career-matching AI.

Your task is to evaluate how well the candidate matches this job.

IMPORTANT:

Analyze MEANING and EXPERIENCE, not just exact keywords.

For example:

"inventory optimization"

and

"optimized stock levels and availability"

may represent the same underlying capability.

Consider:

1. Relevant skills
2. Transferable skills
3. Actual responsibilities
4. Job title relevance
5. Seniority
6. Years of experience
7. Industry experience
8. Technical tools
9. Planning experience
10. Leadership
11. Business exposure
12. Job requirements
13. Career progression
14. Overall suitability

FACTUAL RULE:

Never invent experience.

Never assume the candidate has a skill unless the CV provides reasonable evidence.

A skill can be considered matched when the candidate demonstrates equivalent or transferable experience even if the wording differs.

A skill should be considered missing only when the job genuinely requires it and the CV provides no reasonable evidence of it.

Do not punish the candidate simply because the exact keyword is absent.

Do not reward the candidate simply because a keyword appears without supporting experience.

--------------------------------------------------
CANDIDATE CV
--------------------------------------------------

{cv_text}

--------------------------------------------------
JOB TITLE
--------------------------------------------------

{title}

--------------------------------------------------
COMPANY
--------------------------------------------------

{company}

--------------------------------------------------
LOCATION
--------------------------------------------------

{location}

--------------------------------------------------
JOB DESCRIPTION
--------------------------------------------------

{description}

--------------------------------------------------
SCORING
--------------------------------------------------

Give an overall score from 0 to 100.

90-100:
Exceptional fit. Candidate strongly satisfies the role.

80-89:
Excellent fit. Candidate is highly suitable with only minor gaps.

70-79:
Good fit. Candidate is clearly relevant but has some gaps.

60-69:
Moderate fit. Some strong relevance but meaningful gaps exist.

50-59:
Partial fit. Limited alignment.

0-49:
Weak fit.

Do NOT automatically give high scores.

Be realistic and selective.

--------------------------------------------------
RETURN JSON ONLY
--------------------------------------------------

Return exactly:

{{
    "match_score": 0,

    "match_level": "",

    "matched_skills": [],

    "missing_skills": [],

    "transferable_skills": [],

    "title_match": 0,

    "seniority_match": 0,

    "industry_match": 0,

    "experience_match": 0,

    "technical_match": 0,

    "leadership_match": 0,

    "ranking_reason": "",

    "match_reason": "",

    "strengths": [],

    "gaps": [],

    "recommendation": ""
}}

All scores must be integers from 0 to 100.

Use concise explanations.

Return valid JSON only.
"""


    system_prompt = """
You are CareerAgent's recruitment intelligence engine.

Your job is to objectively compare a candidate's CV against a job.

Use semantic understanding rather than simple keyword matching.

Never fabricate candidate experience.

Never invent skills, responsibilities, achievements or qualifications.

Return valid JSON only.

Accuracy is more important than generosity.
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


        if not isinstance(data, dict):

            return None


        return data


    except Exception as e:

        print(
            "AI job analysis error:",
            e
        )

        return None


# ============================================================
# Main Job Matching Function
# ============================================================

def match_jobs(
    cv_text,
    jobs
):

    if not cv_text:

        return jobs or []


    if not jobs:

        return []


    results = []


    print(
        f"AI analyzing {len(jobs)} jobs..."
    )


    for number, job in enumerate(
        jobs,
        start=1
    ):

        print(
            f"Analyzing job {number}/{len(jobs)}: "
            f"{job.get('job_title', '')}"
        )


        analysis = analyze_job_with_ai(

            cv_text,

            job

        )


        # ====================================================
        # AI Analysis Successful
        # ====================================================

        if analysis:

            job["match_score"] = clean_score(

                analysis.get(
                    "match_score",
                    0
                )

            )


            job["matched_skills"] = safe_list(

                analysis.get(
                    "matched_skills",
                    []
                )

            )


            job["missing_skills"] = safe_list(

                analysis.get(
                    "missing_skills",
                    []
                )

            )


            job["transferable_skills"] = safe_list(

                analysis.get(
                    "transferable_skills",
                    []
                )

            )


            job["title_score"] = clean_score(

                analysis.get(
                    "title_match",
                    0
                )

            )


            job["seniority_score"] = clean_score(

                analysis.get(
                    "seniority_match",
                    0
                )

            )


            job["industry_score"] = clean_score(

                analysis.get(
                    "industry_match",
                    0
                )

            )


            job["experience_score"] = clean_score(

                analysis.get(
                    "experience_match",
                    0
                )

            )


            job["technical_score"] = clean_score(

                analysis.get(
                    "technical_match",
                    0
                )

            )


            job["leadership_score"] = clean_score(

                analysis.get(
                    "leadership_match",
                    0
                )

            )


            job["match_level"] = (

                analysis.get(
                    "match_level",
                    ""
                )

                or

                "AI Match"

            )


            job["match_reason"] = (

                analysis.get(
                    "match_reason",
                    ""
                )

                or

                analysis.get(
                    "ranking_reason",
                    ""
                )

            )


            job["ai_ranking_reason"] = (

                analysis.get(
                    "ranking_reason",
                    ""
                )

            )


            job["strengths"] = safe_list(

                analysis.get(
                    "strengths",
                    []
                )

            )


            job["gaps"] = safe_list(

                analysis.get(
                    "gaps",
                    []
                )

            )


            job["recommendation"] = (

                analysis.get(
                    "recommendation",
                    ""
                )

            )


            job["ai_analyzed"] = True


        # ====================================================
        # AI Failed
        # ====================================================

        else:

            print(
                f"AI analysis failed for: "
                f"{job.get('job_title', '')}"
            )


            # Keep the job instead of crashing
            job["match_score"] = job.get(
                "match_score",
                0
            )


            job["matched_skills"] = job.get(
                "matched_skills",
                []
            )


            job["missing_skills"] = job.get(
                "missing_skills",
                []
            )


            job["transferable_skills"] = []


            job["title_score"] = 0

            job["seniority_score"] = 0

            job["industry_score"] = 0

            job["experience_score"] = 0

            job["technical_score"] = 0

            job["leadership_score"] = 0


            job["match_level"] = (
                "Unable to Analyze"
            )


            job["match_reason"] = (
                "AI analysis could not be completed "
                "for this job."
            )


            job["ai_ranking_reason"] = ""

            job["strengths"] = []

            job["gaps"] = []

            job["recommendation"] = ""

            job["ai_analyzed"] = False


        results.append(
            job
        )


    # ========================================================
    # Sort By AI Score
    # ========================================================

    results.sort(

        key=lambda x: x.get(
            "match_score",
            0
        ),

        reverse=True

    )


    # ========================================================
    # Assign Rank
    # ========================================================

    for rank, job in enumerate(
        results,
        start=1
    ):

        job["rank"] = rank


    print(
        "AI job matching completed."
    )


    return results