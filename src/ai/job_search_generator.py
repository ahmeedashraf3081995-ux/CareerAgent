import json
import requests



def ask_qwen(prompt):

    response = requests.post(

        "http://localhost:11434/api/generate",

        json={

            "model": "qwen2.5:1.5b",

            "prompt": prompt,

            "stream": False,

            "format": "json",

            "options": {

                "temperature": 0

            }

        },

        timeout=300

    )


    response.raise_for_status()


    return response.json()["response"]






def generate_job_search(profile):


    prompt = f"""

You are an expert recruiter and career advisor.

Analyze the candidate CV and create realistic job search parameters.

Your goal is to identify jobs the candidate should apply for.

Do NOT copy the CV words directly.

Convert education, experience, skills, and seniority into realistic LinkedIn job titles.



====================
SENIORITY RULES
====================

Follow strictly:

Fresh graduate:
- Internship
- Training
- Student projects
- Less than 1 year experience

=> seniority_level = "Entry Level"


Less than 3 years relevant full-time experience:

=> seniority_level = "Junior"


3-7 years relevant experience:

=> seniority_level = "Mid Level"


More than 7 years:

=> seniority_level = "Senior Level"



Never recommend:

- Manager
- Senior Manager
- Director
- Head
- Lead

for Entry Level candidates.



====================
SEARCH KEYWORDS RULES
====================


search_keywords MUST contain ONLY job titles.

Generate exactly 5 job titles.

Every item must be a title that can be searched on LinkedIn.


Allowed examples:

- Supply Chain Coordinator
- Procurement Assistant
- Inventory Coordinator
- Operations Coordinator
- Supply Chain Analyst
- Graduate Trainee


Never return:

- Skills
- Software
- Courses
- Training names
- Previous jobs
- Responsibilities
- Industries



Wrong:


[
"Excel",
"Customer Service",
"Finance Training",
"Materials Division",
"Supplier Relationship Management"
]



Correct:


[
"Supply Chain Coordinator",
"Procurement Assistant",
"Inventory Coordinator",
"Operations Coordinator",
"Graduate Trainee"
]




====================
EXCLUDE KEYWORDS
====================

Create keywords that should be avoided.

For Entry Level candidates include:

[
"Manager",
"Senior Manager",
"Director",
"Head",
"Lead"
]




====================
CAREER FIELD
====================

Identify the best career field based on:

- Education
- Work experience
- Training
- Transferable skills




Candidate Profile:


{json.dumps(profile, indent=2)}



Return ONLY JSON:


{{
    "career_field": "",
    "seniority_level": "",
    "search_keywords": [],
    "exclude_keywords": []
}}

"""


    result = json.loads(
        ask_qwen(prompt)
    )



    # ==========================
    # Clean AI output
    # ==========================


    bad_words = [

        "training",
        "experience",
        "skill",
        "excel",
        "customer service",
        "finance",
        "materials division",
        "sales agent",
        "recruiter",
        "tutor",
        "microsoft",
        "office"

    ]



    clean_keywords = []



    for keyword in result.get(
        "search_keywords",
        []
    ):


        if any(

            bad in keyword.lower()

            for bad in bad_words

        ):

            continue



        clean_keywords.append(
            keyword
        )



    result["search_keywords"] = clean_keywords[:5]



    return result






if __name__ == "__main__":


    test_profile = {


        "name": "Candidate",


        "education": [

            "Bachelor of Business Administration",

            "Major: Supply Chain Management"

        ],


        "experience": [

            "Training in Materials Division",

            "Training in Finance Division",

            "Sales Agent",

            "Online Recruiter",

            "Customer Service Representative"

        ],


        "skills": [

            "Supplier Relationship Management",

            "Microsoft Office",

            "Customer Service"

        ]


    }



    print(

        json.dumps(

            generate_job_search(
                test_profile
            ),

            indent=4,

            ensure_ascii=False

        )

    )