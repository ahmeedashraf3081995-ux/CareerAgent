import json
import requests
import os


PROFILE_FILE = "data/profile/profile.json"
JOB_FILE = "data/profile/job_profile.json"
MATCH_FILE = "data/profile/match_report.json"

OUTPUT_FILE = "data/profile/tailored_cv_v2.json"


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def ask_qwen(prompt):

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "qwen3-fast:latest",

            "prompt": prompt,

            "stream": False,

            "format": "json",

            "options": {

                "temperature": 0,

                "num_ctx": 2048

            }

        },

        timeout=600

    )

    response.raise_for_status()

    return response.json()["response"]


def clean_json_response(text):

    """
    Removes markdown or extra text if AI adds it.
    """

    text = text.strip()

    if "```json" in text:

        text = text.replace("```json", "")
        text = text.replace("```", "")

    if "```" in text:

        text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    return text.strip()


def rewrite_cv(profile, job, match):

    prompt = f"""

You are an expert ATS CV writer specialized in Supply Chain and Planning roles.

Rewrite the candidate CV for the target job.

STRICT RULES:

1. Never invent experience.
2. Never add fake companies, tools, achievements, or responsibilities.
3. Keep all numbers and achievements accurate.
4. Rewrite the wording professionally; do not copy original bullets.
5. Use senior Supply Chain language.
6. Focus on business impact.
7. Prioritize experience matching the job description.
8. Keep bullets between 15-30 words.
9. Use ATS keywords naturally.
10. Return ONLY valid JSON. No explanation.


Candidate Profile:

{json.dumps(profile, indent=2)}


Target Job:

{json.dumps(job, indent=2)}


Match Report:

{json.dumps(match, indent=2)}


Return exactly this JSON structure:

{{
    "target_job_title": "",

    "professional_summary": "",

    "skills_section": [
        ""
    ],

    "experience": [
        {{
            "company": "",
            "role": "",
            "rewritten_bullets": [
                ""
            ]
        }}
    ],

    "keywords_added": [
        ""
    ]
}}

"""

    result = ask_qwen(prompt)

    print("\nRAW AI RESPONSE:\n")
    print(result)

    cleaned = clean_json_response(result)

    return json.loads(cleaned)


if __name__ == "__main__":

    profile = load_json(
        PROFILE_FILE
    )

    job = load_json(
        JOB_FILE
    )

    match = load_json(
        MATCH_FILE
    )

    print("Rewriting CV...")

    tailored_cv = rewrite_cv(
        profile,
        job,
        match
    )

    print("\nTAILORED CV:\n")

    print(
        json.dumps(
            tailored_cv,
            indent=4,
            ensure_ascii=False
        )
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tailored_cv,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nTailored CV V2 saved successfully")