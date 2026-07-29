import json
import re
import requests
import sys
import os

from pypdf import PdfReader


# =====================================================
# CONFIG
# =====================================================

QWEN_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:1.5b"

PROFILE_OUTPUT = "data/profile/profile.json"



# =====================================================
# SAVE PROFILE
# =====================================================

def save_profile(profile):

    os.makedirs(
        "data/profile",
        exist_ok=True
    )


    with open(
        PROFILE_OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            indent=2,
            ensure_ascii=False
        )





# =====================================================
# READ CV
# =====================================================

def read_cv(file_path):


    if not os.path.exists(file_path):

        print(
            "CV file not found:",
            file_path
        )

        return ""



    text = ""


    try:


        if file_path.lower().endswith(".pdf"):


            reader = PdfReader(
                file_path
            )


            for page in reader.pages:

                text += (
                    page.extract_text()
                    or ""
                ) + "\n"



        elif file_path.lower().endswith(".txt"):


            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read()



        else:

            print(
                "Only PDF and TXT supported"
            )

            return ""



    except Exception as e:


        print(
            "Reading error:",
            e
        )

        return ""



    return clean_text(text)






# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if not text:
        return ""


    # Fix PDF character spacing
    text = re.sub(
        r'\s+',
        ' ',
        text
    )


    # Join broken single letters
    words = text.split()

    result = []

    buffer = ""


    for word in words:

        if len(word) == 1 and word.isalpha():

            buffer += word

        else:

            if buffer:

                result.append(buffer)
                buffer = ""

            result.append(word)


    if buffer:
        result.append(buffer)


    text = " ".join(result)


    # Restore important spaces
    fixes = {

        "SohilaAshrafAbdalbary":
        "Sohila Ashraf Abdalbary",

        "TraininginMaterialsDivision":
        "Training in Materials Division",

        "TraininginFinanceDivision":
        "Training in Finance Division",

        "Motivatedandresults":
        "Motivated and results",

        "orientedBusiness":
        "oriented Business",

        "Administrationgraduate":
        "Administration graduate",

        "SupplyChain":
        "Supply Chain",

        "ChainManagement":
        "Chain Management",

        "Managementand":
        "Management and",

        "customerservice":
        "customer service",

        "customer servicefunctions":
        "customer service functions"
    }


    for old, new in fixes.items():

        text = text.replace(
            old,
            new
        )

    for old, new in fixes.items():

        text = text.replace(
            old,
            new
        )


    return text.strip()




# =====================================================
# ASK QWEN
# =====================================================

def ask_qwen(prompt):


    try:


        response = requests.post(

            QWEN_URL,

            json={

                "model": MODEL,

                "prompt": prompt,

                "stream": False,

                "format": "json",

                "options": {

                    "temperature":0

                }

            },

            timeout=300

        )


        response.raise_for_status()


        return response.json().get(
            "response",
            "{}"
        )



    except Exception as e:


        print(
            "AI Error:",
            e
        )

        return "{}"






# =====================================================
# SAFE JSON
# =====================================================

def safe_json_parse(text):


    try:

        return json.loads(text)



    except:


        try:

            start = text.index("{")

            end = text.rindex("}") + 1


            return json.loads(
                text[start:end]
            )


        except:


            return {}





# =====================================================
# EXTRACT FACTS
# =====================================================

def extract_cv_facts(text):


    if not text:

        return {}



    prompt=f"""

Extract CV information.

Rules:

Only extract facts.

Never invent.

Return JSON only.


Structure:


{{
"candidate_name":"",
"email":"",
"phone":"",
"location":"",

"education":[],

"work_experience":[],

"skills":[],

"software":[],

"languages":[],

"certifications":[]
}}


CV:

{text}

"""


    return safe_json_parse(
        ask_qwen(prompt)
    )

# =====================================================
# EXPERIENCE CALCULATION
# =====================================================

def calculate_experience(work_experience):


    total_years = 0


    for job in work_experience:


        start = job.get(
            "start_date",
            ""
        )

        end = job.get(
            "end_date",
            ""
        )


        years = re.findall(
            r"\d{4}",
            start + " " + end
        )


        if len(years) >= 2:


            total_years += max(
                0,
                int(years[1]) - int(years[0])
            )



    if total_years >= 7:

        level = "Senior Level"


    elif total_years >= 3:

        level = "Mid Level"


    elif total_years > 0:

        level = "Junior Level"


    else:

        level = "Entry Level"



    return level, f"{total_years} years"







# =====================================================
# CAREER INTELLIGENCE
# =====================================================

def analyse_career(cv_facts):


    prompt=f"""

You are an expert recruiter.

Analyze this candidate.

Use ONLY the provided CV facts.

Do not invent:

- companies
- degrees
- skills
- experience


Prioritize:

1. Education
2. Relevant experience
3. Transferable skills


Generate realistic career direction.


Rules:

Entry Level:

Allowed:

Assistant
Coordinator
Analyst
Associate
Specialist


Never recommend:

Manager
Director
Head
Chief


Return JSON only.


Format:

{{
"career_fields":[],
"career_strengths":[],
"career_gaps":[],
"recommended_job_titles":[]
}}


Candidate:

{json.dumps(cv_facts,indent=2)}

"""


    result = ask_qwen(
        prompt
    )


    return safe_json_parse(
        result
    )








# =====================================================
# PROFILE VALIDATION
# =====================================================

def validate_profile(profile):


    work = profile.get(
        "work_experience",
        []
    )


    level, years = calculate_experience(
        work
    )


    profile["seniority_level"] = level

    profile["years_experience"] = years



    # -----------------------------
    # Career fields cleanup
    # -----------------------------


    fields = profile.get(
        "career_fields",
        []
    )


    if not fields:


        fields = [

            "Supply Chain",

            "Operations"

        ]



    blocked = [

        "teacher",

        "tutor",

        "sales agent",

        "representative"

    ]


    clean=[]


    for field in fields:


        if not any(

            b in field.lower()

            for b in blocked

        ):

            clean.append(
                field
            )



    profile["career_fields"] = clean[:3]






    # -----------------------------
    # Job title cleanup
    # -----------------------------


    jobs = profile.get(
        "recommended_job_titles",
        []
    )


    final_jobs=[]


    forbidden=[

        "manager",

        "director",

        "head",

        "chief"

    ]



    for job in jobs:


        if isinstance(job,dict):

            title = job.get(
                "title",
                ""
            )

        else:

            title = job



        if not title:

            continue



        if any(

            f in title.lower()

            for f in forbidden

        ):

            continue



        final_jobs.append(
            title
        )




    # fallback

    if not final_jobs:


        if "Supply" in str(
            profile["career_fields"]
        ):


            final_jobs=[

                "Supply Chain Coordinator",

                "Supply Chain Analyst",

                "Procurement Assistant",

                "Inventory Coordinator",

                "Operations Coordinator"

            ]


        else:


            final_jobs=[

                "Operations Assistant",

                "Customer Service Specialist",

                "Administrative Assistant"

            ]



    profile["recommended_job_titles"] = list(
        dict.fromkeys(final_jobs)
    )[:8]



    # LinkedIn search terms

    profile["linkedin_search_keywords"] = profile[
        "recommended_job_titles"
    ]



    profile["excluded_job_titles"]=[

        "Manager",

        "Director",

        "Head"

    ]



    return profile






# =====================================================
# FINAL PIPELINE
# =====================================================

def extract_profile(text):


    facts = extract_cv_facts(
        text
    )


    career = analyse_career(
        facts
    )


    profile = {

        **facts,

        **career

    }


    return validate_profile(
        profile
    )






# =====================================================
# RUN FROM POWERSHELL
# =====================================================

if __name__ == "__main__":


    if len(sys.argv) < 2:


        print(
            """
Usage:

python src\\cv\\cv_reader.py "CV_FILE.pdf"

Example:

python src\\cv\\cv_reader.py "Sohilaa_CV.pdf.pdf"
"""
        )

        sys.exit()



    cv_file = sys.argv[1]



    print(
        "\nReading:",
        cv_file
    )



    text = read_cv(
        cv_file
    )



    if not text:


        print(
            "No CV text extracted"
        )

        sys.exit()



    profile = extract_profile(
        text
    )



    save_profile(
        profile
    )



    print(
        "\nPROFILE GENERATED\n"
    )


    print(

        json.dumps(

            profile,

            indent=2,

            ensure_ascii=False

        )

    )


    print(
        "\nSaved to:",
        PROFILE_OUTPUT
    )