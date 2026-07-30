from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# AI Job Ranker
# ============================================================

def rank_jobs_with_ai(
    cv_text,
    jobs
):

    if not jobs:
        return []


    # ========================================================
    # Prepare Compact Job Data
    # ========================================================

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

            "match_score":
                job.get(
                    "match_score",
                    0
                ),

            "matched_skills":
                job.get(
                    "matched_skills",
                    []
                ),

            "missing_skills":
                job.get(
                    "missing_skills",
                    []
                ),

            "transferable_skills":
                job.get(
                    "transferable_skills",
                    []
                ),

            "title_score":
                job.get(
                    "title_score",
                    0
                ),

            "seniority_score":
                job.get(
                    "seniority_score",
                    0
                ),

            "industry_score":
                job.get(
                    "industry_score",
                    0
                ),

            "experience_score":
                job.get(
                    "experience_score",
                    0
                ),

            "technical_score":
                job.get(
                    "technical_score",
                    0
                ),

            "leadership_score":
                job.get(
                    "leadership_score",
                    0
                ),

            "strengths":
                job.get(
                    "strengths",
                    []
                ),

            "gaps":
                job.get(
                    "gaps",
                    []
                ),

            "recommendation":
                job.get(
                    "recommendation",
                    ""
                )

        })


    # ========================================================
    # AI Ranking Prompt
    # ========================================================

    prompt = f"""
You are CareerAgent's senior recruitment ranking engine.

You have already received individual AI analysis for every job.

Your task is to rank ALL jobs against the candidate's CV.

Do NOT re-analyze the full job descriptions.

Use the structured analysis provided for each job.

Consider:

- Overall career fit
- Relevant experience
- Transferable experience
- Skills
- Missing skills
- Seniority
- Career progression
- Industry
- Technical tools
- Planning experience
- Leadership
- Existing match score
- Strengths
- Gaps
- Realistic suitability

IMPORTANT:

Do not simply sort by match_score.

Use professional recruitment judgment.

Do not invent candidate experience.

A job with a slightly lower technical score may still be a better
career opportunity because of title, seniority, progression,
responsibility or overall fit.

--------------------------------------------------
CANDIDATE CV
--------------------------------------------------

{cv_text}

--------------------------------------------------
ANALYZED JOBS
--------------------------------------------------

{job_data}

--------------------------------------------------
RETURN JSON ONLY
--------------------------------------------------

Return ALL jobs.

Use exactly:

{{
    "ranked_jobs": [

        {{
            "index": 0,

            "ai_score": 0,

            "ranking_reason": "",

            "best_fit": false,

            "priority": "High",

            "recommendation": ""
        }}

    ]
}}

Rules:

ai_score must be between 0 and 100.

100 = exceptional career opportunity.

best_fit = true ONLY for the strongest opportunities.

priority must be exactly:

"High"
"Medium"
"Low"

Return one ranking result for every job.

Do not omit jobs.

Return valid JSON only.
"""


    system_prompt = """
You are CareerAgent's senior recruitment ranking AI.

You compare multiple already-analyzed job opportunities
against one candidate.

Use professional recruitment judgment.

Use semantic understanding.

Never fabricate candidate experience.

Never rank a job highly simply because of keyword overlap.

Return valid JSON only.
"""


    # ========================================================
    # AI Call
    # ========================================================

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


    except Exception as e:

        print(
            "AI ranking error:",
            e
        )

        return jobs


    if not isinstance(
        data,
        dict
    ):

        print(
            "AI ranking returned invalid data."
        )

        return jobs


    rankings = data.get(
        "ranked_jobs",
        []
    )


    if not isinstance(
        rankings,
        list
    ):

        print(
            "AI ranking returned no ranked jobs."
        )

        return jobs


    ranking_map = {}


    # ========================================================
    # Parse Rankings
    # ========================================================

    for item in rankings:

        if not isinstance(
            item,
            dict
        ):

            continue


        try:

            index = int(

                item.get(
                    "index",
                    -1
                )

            )

        except Exception:

            continue


        if index < 0 or index >= len(jobs):

            continue


        try:

            ai_score = int(

                float(

                    item.get(
                        "ai_score",
                        0
                    )

                )

            )

        except Exception:

            ai_score = 0


        ai_score = max(

            0,

            min(
                100,
                ai_score
            )

        )


        priority = item.get(
            "priority",
            "Medium"
        )


        if priority not in [

            "High",
            "Medium",
            "Low"

        ]:

            priority = "Medium"


        ranking_map[index] = {

            "ai_score":
                ai_score,

            "ranking_reason":
                item.get(
                    "ranking_reason",
                    ""
                ),

            "best_fit":
                bool(
                    item.get(
                        "best_fit",
                        False
                    )
                ),

            "priority":
                priority,

            "recommendation":
                item.get(
                    "recommendation",
                    ""
                )

        }


    # ========================================================
    # Apply Ranking
    # ========================================================

    for index, job in enumerate(
        jobs
    ):

        ranking = ranking_map.get(
            index
        )


        if ranking:

            job["ai_score"] = (

                ranking[
                    "ai_score"
                ]

            )


            job["ai_ranking_reason"] = (

                ranking[
                    "ranking_reason"
                ]

            )


            job["ai_best_fit"] = (

                ranking[
                    "best_fit"
                ]

            )


            job["ai_priority"] = (

                ranking[
                    "priority"
                ]

            )


            job["ai_recommendation"] = (

                ranking[
                    "recommendation"
                ]

            )


            # AI ranking becomes final score

            job["match_score"] = (

                ranking[
                    "ai_score"
                ]

            )


        else:

            # Keep original matcher score

            job["ai_score"] = job.get(

                "match_score",

                0

            )


            job["ai_ranking_reason"] = ""

            job["ai_best_fit"] = False

            job["ai_priority"] = "Medium"

            job["ai_recommendation"] = ""


    # ========================================================
    # Sort
    # ========================================================

    jobs.sort(

        key=lambda x: x.get(

            "ai_score",

            x.get(
                "match_score",
                0
            )

        ),

        reverse=True

    )


    # ========================================================
    # Assign Final Rank
    # ========================================================

    for rank, job in enumerate(

        jobs,

        start=1

    ):

        job["rank"] = rank


        score = job.get(

            "ai_score",

            job.get(
                "match_score",
                0
            )

        )


        # ----------------------------------------------------
        # Match Level
        # ----------------------------------------------------

        if score >= 90:

            job["match_level"] = (
                "🔥 Exceptional Match"
            )

        elif score >= 80:

            job["match_level"] = (
                "🔥 Excellent Match"
            )

        elif score >= 70:

            job["match_level"] = (
                "✅ Good Match"
            )

        elif score >= 60:

            job["match_level"] = (
                "⚠️ Moderate Match"
            )

        elif score >= 50:

            job["match_level"] = (
                "⚠️ Partial Match"
            )

        else:

            job["match_level"] = (
                "❌ Weak Match"
            )


    print(
        "AI ranking completed."
    )


    return jobs