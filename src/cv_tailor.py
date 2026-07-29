import json
import requests
import os


PROFILE_FILE = "data/profile/profile.json"
OUTPUT_FILE = "data/profile/tailored_cv.json"


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

            "model": "qwen2.5:1.5b",

            "prompt": prompt,

            "stream": False,

            "format": "json",

            "options": {

                "temperature": 0,

                "num_ctx": 4096

            }

        },

        timeout=300

    )


    response.raise_for_status()

    return response.json()["response"]




def create_tailored_cv(
    profile,
    job
):


    prompt = f"""

You are an expert ATS CV optimization assistant.

Optimize this candidate profile for the target job.

Rules:

- Never invent experience.
- Never create fake achievements.
- Only use information from the candidate profile.
- Suggest realistic improvements.
- Focus on ATS keywords.


Candidate Profile:

{json.dumps(profile, indent=2)}


Target Job:

{json.dumps(job, indent=2)}



Return ONLY JSON:

{{
"target_role":"",
"summary_improvement":"",
"keywords_to_emphasize":[],
"experience_focus":[
    {{
        "company":"",
        "points_to_highlight":[]
    }}
],
"skills_to_prioritize":[],
"cover_letter_angles":[],
"interview_questions":[]
}}

"""


    result = ask_qwen(
        prompt
    )


    return json.loads(
        result
    )





def tailor_from_dashboard(job):


    profile = load_json(
        PROFILE_FILE
    )


    tailored = create_tailored_cv(
        profile,
        job
    )


    os.makedirs(
        "data/profile",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            tailored,
            file,
            indent=4,
            ensure_ascii=False
        )


    return tailored




if __name__ == "__main__":


    profile = load_json(
        PROFILE_FILE
    )


    job = load_json(
        "data/profile/job_profile.json"
    )


    result = create_tailored_cv(
        profile,
        job
    )


    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )