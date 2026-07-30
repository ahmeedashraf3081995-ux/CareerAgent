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
    # Prepare Job Data
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

            "description":
                job.get(
                    "description",
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
                )

        })


    prompt = f"""
You are CareerAgent's senior recruitment ranking engine.

Rank ALL jobs against the candidate's CV.

The jobs have already received individual AI match analysis.

Your task is to compare them and determine which opportunities
are genuinely strongest for this candidate.

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
- Job responsibilities
- Job requirements
- Quality of opportunity
- Realistic suitability

Do not simply rank by the existing match score.

Use your own professional judgment.

Do not invent candidate experience.

CV:

----------------

{cv_text}

----------------

JOBS:

----------------

{job_data}

----------------

Return ALL jobs.

Return ONLY JSON.

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

ai_score must be 0-100.

100 = exceptional career opportunity.

best_fit should be true only for the strongest opportunities.

priority must be one of:

"High"
"Medium"
"Low"

Be selective.

Return valid JSON only.
"""


    system_prompt = """
You are CareerAgent's senior recruitment ranking AI.

You compare multiple job opportunities against a candidate.

Use semantic understanding and professional recruitment judgment.

Never fabricate candidate experience.

Never reward a job simply because it contains matching keywords.

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
            "AI ranking error:",
            e
        )

        return jobs


    rankings = data.get(
        "ranked_jobs",
        []
    )


    ranking_map = {}


    # ========================================================
    # Parse Rankings
    # ========================================================

    for item in rankings:

        try:

            index = int(

                item.get(
                    "index",
                    -1
                )

            )

        except Exception:

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
                item.get(
                    "priority",
                    "Medium"
                ),

            "recommendation":
                item.get(
                    "recommendation",
                    ""
                )

        }


    # ========================================================
    # Apply AI Ranking
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


            # ------------------------------------------------
            # AI ranking becomes the primary score
            # ------------------------------------------------

            job["match_score"] = (

                ranking[
                    "ai_score"
                ]

            )


        else:

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