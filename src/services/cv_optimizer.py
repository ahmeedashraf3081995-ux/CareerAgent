import json
import re

from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# Text Helpers
# ============================================================

def clean_text(text):

    if not text:

        return ""

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


def safe_list(value):

    if isinstance(
        value,
        list
    ):

        return value

    return []


def tokenize(text):

    return set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#&.-]{2,}\b",
            text.lower()
        )
    )


# ============================================================
# ATS Score
# ============================================================

def calculate_ats_score(
    cv_text,
    target_job="",
    job_description=""
):

    cv_text = clean_text(
        cv_text
    )

    target_job = clean_text(
        target_job
    )

    job_description = clean_text(
        job_description
    )

    if not cv_text:

        return 0

    cv_lower = cv_text.lower()

    score = 0


    # ========================================================
    # 1. CV Structure
    # ========================================================

    standard_sections = [

        "summary",
        "professional summary",
        "experience",
        "work experience",
        "professional experience",
        "education",
        "skills",
        "certifications",
        "projects"

    ]

    found_sections = 0

    for section in standard_sections:

        if section in cv_lower:

            found_sections += 1

    score += min(
        found_sections * 3,
        20
    )


    # ========================================================
    # 2. Contact Information
    # ========================================================

    if re.search(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        cv_text
    ):

        score += 5


    if re.search(
        r"\+?\d[\d\s\-\(\)]{7,}",
        cv_text
    ):

        score += 5


    # ========================================================
    # 3. Quantification
    # ========================================================

    numbers = re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        cv_text
    )


    if len(numbers) >= 10:

        score += 10

    elif len(numbers) >= 5:

        score += 7

    elif len(numbers) >= 2:

        score += 4


    # ========================================================
    # 4. Keyword Match
    # ========================================================

    reference_text = (
        target_job
        + " "
        + job_description
    ).strip()


    if reference_text:

        reference_words = tokenize(
            reference_text
        )


        stop_words = {

            "the",
            "and",
            "for",
            "with",
            "from",
            "this",
            "that",
            "your",
            "our",
            "you",
            "are",
            "will",
            "have",
            "has",
            "job",
            "role",
            "work",
            "working",
            "years",
            "year"

        }


        reference_words = {

            word
            for word in reference_words
            if word not in stop_words

        }


        if reference_words:

            matched = sum(

                1
                for word in reference_words
                if word in cv_lower

            )


            keyword_ratio = (

                matched
                /
                len(reference_words)

            )


            score += round(

                min(

                    keyword_ratio * 35,
                    35

                )

            )


    # ========================================================
    # 5. CV Length
    # ========================================================

    if len(cv_text) >= 1500:

        score += 5


    if len(cv_text) >= 3000:

        score += 5


    # ========================================================
    # 6. Action Language
    # ========================================================

    action_words = [

        "managed",
        "led",
        "developed",
        "implemented",
        "optimized",
        "improved",
        "analyzed",
        "created",
        "delivered",
        "increased",
        "reduced",
        "launched",
        "coordinated",
        "forecasted",
        "planned"

    ]


    action_count = sum(

        1
        for word in action_words
        if word in cv_lower

    )


    if action_count >= 8:

        score += 10

    elif action_count >= 4:

        score += 6

    elif action_count >= 2:

        score += 3


    return min(
        score,
        100
    )


# ============================================================
# AI CV Generation
# ============================================================

def generate_cv(
    cv_text,
    target_job="",
    job_description="",
    user_instructions="",
    conversation=""
):

    prompt = f"""
You are an expert CV writer, recruiter and ATS optimization specialist.

You are working inside CareerAgent.

Your task is to improve the candidate's CV.

IMPORTANT FACTUAL RULES:

NEVER invent factual information.

Do NOT invent:

- employers
- job titles
- dates
- education
- certifications
- achievements
- responsibilities
- technologies
- skills
- metrics
- business results
- languages
- locations

Only use information supported by the original CV.

You may improve wording, structure, clarity and professionalism.

You may tailor wording to the target role.

You may use keywords from the job description ONLY when the
candidate's existing experience supports those keywords.

If something requested by the user is not supported by the CV,
do NOT add it as fact.

Instead, mention it in the warnings array.

CURRENT CV:
----------------
{cv_text}
----------------

TARGET JOB:
{target_job or "Not Provided"}

JOB DESCRIPTION:
----------------
{job_description or "Not Provided"}
----------------

USER INSTRUCTIONS:
----------------
{user_instructions or "No Additional Instructions"}
----------------

PREVIOUS CONVERSATION:
----------------
{conversation or "None"}
----------------


OBJECTIVES:

1. Create a professional ATS-friendly CV.

2. Preserve factual experience.

3. Improve wording.

4. Use strong action verbs.

5. Improve weak bullet points.

6. Preserve existing numbers.

7. Never fabricate numbers.

8. Never fabricate skills.

9. Never fabricate responsibilities.

10. Tailor the CV to the target role when provided.

11. Use relevant job-description keywords when supported.

12. Remove unnecessary wording.

13. Remove repetition.

14. Improve the professional summary.

15. Improve the skills section using supported skills.

16. Keep the CV concise.

17. Use standard ATS-friendly section names.

18. Use plain text.

19. Do not use tables.

20. Do not use columns.

21. Do not use graphics.

22. Do not use icons.

23. Do not use emojis.

24. Do not add references unless already present.

25. Do not add unsupported information.


CV STRUCTURE:

NAME

CONTACT INFORMATION

PROFESSIONAL SUMMARY

CORE SKILLS

PROFESSIONAL EXPERIENCE

EDUCATION

CERTIFICATIONS

ADDITIONAL INFORMATION

Only include sections supported by the original CV.


BULLETS:

Use bullet points for experience.

Prefer:

Action + responsibility + result

when the original CV supports the result.

Never invent a result.


RETURN ONLY JSON.

Use exactly this structure:

{{
    "cv_text": "FULL UPDATED CV HERE",
    "summary": "SHORT DESCRIPTION OF WHAT WAS IMPROVED",
    "changes": [
        "Change 1",
        "Change 2",
        "Change 3"
    ],
    "warnings": [
        "Anything requiring confirmation"
    ]
}}
"""


    system_prompt = """
You are CareerAgent's CV optimization engine.

Accuracy is more important than creativity.

Never fabricate candidate information.

Return valid JSON only.

Do not include markdown outside the JSON.
"""


    # ========================================================
    # Ask Local Ollama AI
    # ========================================================

    content = ask_ollama(

        prompt,

        system_prompt=system_prompt,

        temperature=0.1,

        json_mode=True

    )


    # ========================================================
    # Extract JSON
    # ========================================================

    data = extract_json(
        content
    )


    # ========================================================
    # CV Result
    # ========================================================

    cv_result = data.get(
        "cv_text",
        ""
    )


    if not cv_result:

        cv_result = cv_text


    return {

        "cv_text": cv_result,

        "summary": data.get(
            "summary",
            ""
        ),

        "changes": safe_list(
            data.get(
                "changes",
                []
            )
        ),

        "warnings": safe_list(
            data.get(
                "warnings",
                []
            )
        )

    }


# ============================================================
# Optimize CV
# ============================================================

def optimize_cv(
    cv_text,
    target_job="",
    job_description="",
    user_instructions="",
    conversation=""
):

    before_score = calculate_ats_score(

        cv_text,

        target_job,

        job_description

    )


    result = generate_cv(

        cv_text,

        target_job,

        job_description,

        user_instructions,

        conversation

    )


    after_score = calculate_ats_score(

        result["cv_text"],

        target_job,

        job_description

    )


    result["before_score"] = before_score

    result["after_score"] = after_score

    result["score_change"] = (

        after_score
        -
        before_score

    )


    return result