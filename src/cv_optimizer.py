import json
import requests
import os
import re


CV_FILE = "data/profile/profile.json"
JOB_FILE = "data/profile/job_profile.json"

OUTPUT_FILE = "data/profile/cv_optimization.json"


def load_json(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def ask_ai(prompt):

    print("Sending request to AI...")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_ctx": 2048
            }
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    result = data.get("response", "")

    print("\nRAW AI RESPONSE:")
    print(result)

    if not result:
        raise Exception("Empty AI response")

    return result


def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise Exception(
            "No JSON found in AI response"
        )

    return json.loads(
        match.group()
    )


def optimize_cv(cv, job):

    prompt = f"""

You are an ATS CV optimizer.

Analyze the candidate CV against the job.

Rules:
- Do not remove information.
- Do not invent experience.
- Suggest only improvements.
- Return JSON only.

Format:

{{
"summary_improvement":"",
"keywords_to_emphasize":[],
"bullet_improvements":[]
}}

CV:

Name:
{cv.get("name","")}

Skills:
{json.dumps(cv.get("skills",[]))}

Experience:
{json.dumps(cv.get("companies",[]))}


JOB:

Title:
{job.get("job_title","")}

Skills:
{json.dumps(job.get("required_skills",[]))}

Keywords:
{json.dumps(job.get("keywords",[]))}

"""


    result = ask_ai(prompt)

    return extract_json(result)


if __name__ == "__main__":

    print("Analyzing CV against job...")

    cv = load_json(CV_FILE)

    job = load_json(JOB_FILE)

    optimization = optimize_cv(
        cv,
        job
    )

    print("\nCV OPTIMIZATION:")

    print(
        json.dumps(
            optimization,
            indent=4,
            ensure_ascii=False
        )
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            optimization,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("\nOptimization saved successfully")