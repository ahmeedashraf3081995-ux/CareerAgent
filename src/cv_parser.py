import requests
import json
import os


CV_FILE = "data/profile/Ahmed_CV.txt"
OUTPUT_FILE = "data/profile/profile.json"


def read_cv():

    print("Reading CV TXT...")

    with open(
        CV_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def ask_qwen(prompt):

    print("Sending CV to AI...")

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


def create_profile(cv_text):

    prompt = f"""
You are a professional CV parser.

Extract structured information from the CV below.

Return ONLY valid JSON.
No explanation.
No markdown.

Use exactly this JSON structure:

{{
    "name": "",
    "current_company": "",
    "current_role": "",
    "years_experience": "",
    "companies": [],
    "skills": [],
    "tools": [],
    "education": [],
    "responsibilities": [],
    "achievements": []
}}

Rules:

- Use ONLY information available in the CV.
- Never invent companies, responsibilities, achievements, skills, or tools.
- The current company is the company with the latest employment date ending with "Present".
- The current role is the job title connected to that company.
- Extract all previous companies with their correct job titles.
- Tools means software, systems, and technical tools only:
  Examples: SAP, Excel, Power BI, Tableau, Python, SQL.
- Skills means professional capabilities only:
  Examples: Demand Planning, Forecasting, Inventory Optimization, S&OP.
- Responsibilities must contain actual bullet points from work experience.
- Achievements must contain only measurable results or named projects mentioned in the CV.
- Keep numbers and percentages exactly as written.
- Do not summarize responsibilities.

CV:

{cv_text}
"""

    result = ask_qwen(prompt)

    return json.loads(result)


if __name__ == "__main__":

    cv_text = read_cv()

    profile = create_profile(cv_text)

    print("\nJSON OUTPUT:\n")

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

    print("\nProfile saved successfully")