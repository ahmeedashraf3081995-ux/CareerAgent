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
# Analyze One Batch Of Jobs
# ============================================================

def analyze_job_batch_with_ai(
    cv_text,
    jobs
):

    if not jobs:
        return []


    job_data = []


    for index, job in enumerate(jobs):

        job_data.append({

            "index":
                index,

            "job_title":
                job.get(
                    "job_title",
                    ""
                ),

            "company":
                job.get(
                    "company",
                    ""
                ),

            "location":
                job.get(
                    "location",
                    ""
                ),

            "description":
                job.get(
                    "description",
                    ""
                )

        })


    prompt = f"""
You are CareerAgent's expert recruitment and career-matching AI.

Analyze ALL jobs below against the candidate's CV.

You must analyze each job independently.

IMPORTANT:

Analyze meaning and experience, not just exact keywords.

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

FACTUAL RULES:

Never invent experience.

Never assume the candidate has a skill unless the CV provides reasonable evidence.

A skill can be considered matched when the candidate demonstrates equivalent or transferable experience.

A skill should be considered missing only when the job genuinely requires it and the CV provides no reasonable evidence.

Do not punish the candidate simply because the exact keyword is absent.

Do not reward the candidate simply because a keyword appears without supporting experience.

--------------------------------------------------
CANDIDATE CV
--------------------------------------------------

{cv_text}

--------------------------------------------------
JOBS
--------------------------------------------------

{json.dumps(job_data, ensure_ascii=False)}

--------------------------------------------------
SCORING
--------------------------------------------------

Give an overall score from 0 to 100.

90-100:
Exceptional fit.

80-89:
Excellent fit.

70-79:
Good fit.

60-69:
Moderate fit.

50-59:
Partial fit.

0-49:
Weak fit.

Be realistic and selective.

--------------------------------------------------
RETURN JSON ONLY
--------------------------------------------------

Return exactly this structure:

{{
    "jobs": [

        {{
            "index": 0,

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

    ]
}}

IMPORTANT:

Return exactly ONE result for EVERY job.

The "index" must correspond to the job index provided above.

All scores must be integers from 0 to 100.

Use concise explanations.

Return valid JSON only.
"""


    system_prompt = """
You are CareerAgent's recruitment intelligence engine.

Analyze multiple jobs against one candidate CV.

Use semantic understanding rather than simple keyword matching.

Never fabricate candidate experience.

Analyze every supplied job.

Return valid JSON only.

Accuracy is more important than generosity.
"""


    try:

        response = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0,

            json_mode=True

        )


        data = extract_json(
            response
        )


        if not isinstance(
            data,
            dict
        ):

            return []


        results = data.get(
            "jobs",
            []
        )


        if not isinstance(
            results,
            list
        ):

            return []


        return results


    except Exception as e:

        print(
            "AI batch analysis error:",
            e
        )

        return []


# ============================================================
# Apply AI Analysis
# ============================================================

def apply_analysis(
    job,
    analysis
):

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


    return job


# ============================================================
# Main Job Matching Function
# ============================================================

def match_jobs(
    cv_text,
    jobs,
    batch_size=10
):

    if not cv_text:

        return jobs or []


    if not jobs:

        return []


    results = []


    total_jobs = len(jobs)

    total_batches = (

        (total_jobs + batch_size - 1)
        // batch_size

    )


    print(
        f"AI analyzing {total_jobs} jobs "
        f"in {total_batches} batches..."
    )


    # ========================================================
    # Process Jobs In Batches
    # ========================================================

    for batch_number, start in enumerate(

        range(
            0,
            total_jobs,
            batch_size
        ),

        start=1

    ):

        batch = jobs[

            start:
            start + batch_size

        ]


        print(

            f"Analyzing batch "
            f"{batch_number}/{total_batches} "
            f"({len(batch)} jobs)..."

        )


        analyses = analyze_job_batch_with_ai(

            cv_text,

            batch

        )


        # ----------------------------------------------------
        # Create Analysis Map
        # ----------------------------------------------------

        analysis_map = {}


        for analysis in analyses:

            if not isinstance(
                analysis,
                dict
            ):

                continue


            try:

                index = int(

                    analysis.get(
                        "index",
                        -1
                    )

                )

            except Exception:

                continue


            if 0 <= index < len(batch):

                analysis_map[index] = analysis


        # ----------------------------------------------------
        # Apply Results
        # ----------------------------------------------------

        for index, job in enumerate(
            batch
        ):

            analysis = analysis_map.get(
                index
            )


            if analysis:

                job = apply_analysis(

                    job,

                    analysis

                )


            else:

                print(

                    "AI analysis missing for:",

                    job.get(
                        "job_title",
                        ""
                    )

                )


                job["match_score"] = 0

                job["matched_skills"] = []

                job["missing_skills"] = []

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
                    "AI analysis could not be "
                    "completed for this job."
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
    # Sort By Match Score
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
        "AI batch job matching completed."
    )


    return results