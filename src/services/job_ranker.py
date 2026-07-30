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
    # Prepare Jobs
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
                )

        })


    prompt = f"""
You are CareerAgent's senior recruitment ranking engine.

Rank the jobs against the candidate's CV.

The objective is NOT simply to find jobs with similar titles.

Consider:

- Actual transferable experience
- Skills
- Responsibilities
- Seniority
- Industry
- Years of experience
- Leadership
- Technical tools
- Planning experience
- Business exposure
- Job requirements
- Overall career fit

Do NOT invent experience.

Do NOT assume the candidate has a skill unless supported by the CV.

CV:
----------------
{cv_text}
----------------

JOBS:
----------------
{job_data}
----------------

Return ONLY JSON:

{{
    "ranked_jobs": [
        {{
            "index": 0,
            "ai_score": 0,
            "ranking_reason": "",
            "best_fit": true
        }}
    ]
}}

Rank ALL jobs.

Use 0-100 for ai_score.

100 means an exceptional fit.

Be realistic and selective.
"""


    system_prompt = """
You are CareerAgent's senior recruitment AI.

You rank candidates against jobs objectively.

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
            "AI ranking error:",
            e
        )

        return jobs


    rankings = data.get(
        "ranked_jobs",
        []
    )


    ranking_map = {}


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


        ranking_map[index] = {

            "ai_score":
                max(
                    0,
                    min(
                        100,
                        int(
                            item.get(
                                "ai_score",
                                0
                            )
                        )
                    )
                ),

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
                )

        }


    # ========================================================
    # Apply AI Ranking
    # ========================================================

    for index, job in enumerate(jobs):

        ranking = ranking_map.get(
            index
        )


        if ranking:

            job["ai_score"] = (
                ranking["ai_score"]
            )

            job["ai_ranking_reason"] = (
                ranking["ranking_reason"]
            )

            job["ai_best_fit"] = (
                ranking["best_fit"]
            )

        else:

            job["ai_score"] = (
                job.get(
                    "match_score",
                    0
                )
            )

            job["ai_ranking_reason"] = ""

            job["ai_best_fit"] = False


        # ----------------------------------------------------
        # Combine Existing Match + AI
        # ----------------------------------------------------

        existing_score = job.get(
            "match_score",
            0
        )


        ai_score = job.get(
            "ai_score",
            existing_score
        )


        final_score = round(

            (
                existing_score
                * 0.30
            )

            +

            (
                ai_score
                * 0.70
            )

        )


        job["match_score"] = max(

            0,

            min(
                100,
                final_score
            )

        )


    # ========================================================
    # Sort
    # ========================================================

    jobs.sort(

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
        jobs,
        start=1
    ):

        job["rank"] = rank


        score = job.get(
            "match_score",
            0
        )


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


    return jobs