import requests
import json
import os


OUTPUT_FILE = "data/profile/job_profile.json"


def ask_qwen(prompt):

    print("Sending job description to AI...")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_ctx": 2048
            }
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


def parse_job(job_text):

    prompt = f"""
You are a job description parser.

Extract information from the job description below.

Return ONLY JSON.

Use this structure:

{{
    "job_title": "",
    "company": "",
    "location": "",
    "seniority": "",
    "years_experience_required": "",
    "required_skills": [],
    "required_tools": [],
    "keywords": [],
    "responsibilities": []
}}

Rules:
- Use only information from the job description.
- Do not invent requirements.
- Separate skills from software/tools.
- Extract important ATS keywords.
- Keep responsibilities as written.

JOB DESCRIPTION:

{job_text}
"""

    result = ask_qwen(prompt)

    return json.loads(result)


if __name__ == "__main__":

    print("Paste job description below.")
    print("When finished type: END")

    lines = []

    while True:
        line = input()

        if line == "END":
            break

        lines.append(line)


    job_text = "\n".join(lines)

    profile = parse_job(job_text)


    print("\nJOB PROFILE:\n")

    print(
        json.dumps(
            profile,
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
            profile,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("\nJob profile saved successfully")