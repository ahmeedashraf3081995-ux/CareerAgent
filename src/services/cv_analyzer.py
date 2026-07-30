from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# AI CV Analyzer
# ============================================================

def analyze_cv(text):

    if not text:

        return {

            "job_titles": [],

            "countries": [],

            "cities": [],

            "companies": [],

            "skills": [],

            "years_experience": 0,

            "industries": []

        }


    prompt = f"""
Analyze the following CV as an expert recruiter.

Your job is to identify realistic job-search criteria based
ONLY on information actually present in the CV.

Do not invent information.

Identify:

1. Current and previous job titles.
2. Reasonable target job titles based on the candidate's actual
   experience.
3. Countries explicitly appearing in the CV.
4. Cities explicitly appearing in the CV.
5. Companies explicitly appearing in the CV.
6. Professional skills explicitly supported by the CV.
7. Approximate years of professional experience if clearly
   supported.
8. Industries supported by the CV.

IMPORTANT:

- Do not invent employers.
- Do not invent job titles.
- Do not invent locations.
- Do not infer a country merely because a company is famous there.
- Target roles should be realistic extensions of the candidate's
  existing experience.
- Return concise values.
- Avoid duplicate values.

CV:
----------------
{text}
----------------

Return ONLY valid JSON using exactly:

{{
    "job_titles": [],
    "countries": [],
    "cities": [],
    "companies": [],
    "skills": [],
    "years_experience": 0,
    "industries": []
}}
"""


    system_prompt = """
You are CareerAgent's CV analysis engine.

Accuracy is more important than creativity.

Never fabricate candidate information.

Return valid JSON only.
"""


    response = ask_ollama(

        prompt,

        system_prompt=system_prompt,

        temperature=0.1,

        json_mode=True

    )


    data = extract_json(
        response
    )


    return {

        "job_titles":
            data.get(
                "job_titles",
                []
            ),

        "countries":
            data.get(
                "countries",
                []
            ),

        "cities":
            data.get(
                "cities",
                []
            ),

        "companies":
            data.get(
                "companies",
                []
            ),

        "skills":
            data.get(
                "skills",
                []
            ),

        "years_experience":
            data.get(
                "years_experience",
                0
            ),

        "industries":
            data.get(
                "industries",
                []
            )

    }