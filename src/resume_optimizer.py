from ai_assistant import ask_qwen
import json


def load_profile():
    with open(
        "data/profile/user_profile.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def optimize_resume(job):

    user = load_profile()

    prompt = f"""
You are a professional CV optimization assistant.

Your task is to suggest MINOR CV improvements for a job application.

STRICT RULES:
- Never invent experience.
- Never create achievements.
- Never create numbers or percentages.
- Never create team sizes.
- Never add companies the candidate did not work for.
- Only use information available in the candidate profile.
- If something is missing, say "Not available in profile".

You can only:
1. Improve CV headline.
2. Suggest skills to highlight.
3. Suggest keywords from the job.
4. Suggest wording improvements using existing experience.

Candidate Profile:

{json.dumps(user, indent=2)}

Target Job:

Company:
{job['company']}

Title:
{job['title']}

Location:
{job['location']}

Job Skills:
{job['skills']}


Create a report:

Resume Optimization Report
==========================

Recommended CV Headline:

Skills to Highlight:

Keywords to Add:

Experience Wording Suggestions:

Interview Positioning:

Remember: do not invent anything.
"""

    response = ask_qwen(prompt)

    return response


if __name__ == "__main__":

    test_job = {
        "company": "Amazon",
        "title": "Senior Demand Planner",
        "location": "Calgary",
        "skills": [
            "Demand Forecasting",
            "S&OP",
            "Inventory Optimization",
            "SAP"
        ]
    }

    result = optimize_resume(test_job)

    print("==========================")
    print(result)