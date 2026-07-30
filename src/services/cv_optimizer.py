import os
import json
import re

from openai import OpenAI


# ============================================================
# OpenAI Client
# ============================================================

def get_client():

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "OPENAI_API_KEY is not configured."
        )

    return OpenAI(
        api_key=api_key
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

    # Maximum 20 points

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
    # 3. Achievement / Quantification
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
    # 4. Target Job / JD Keyword Match
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

        # Remove extremely generic words

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
                matched /
                len(reference_words)
            )

            score += round(
                min(
                    keyword_ratio * 35,
                    35
                )
            )

    # ========================================================
    # 5. CV Length / Content
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

    client = get_client()

    prompt = f"""
You are an expert CV writer, recruiter and ATS optimization specialist.

Your task is to improve the candidate's CV.

CRITICAL RULE:

NEVER invent or assume factual information.

Do not invent:

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

If the user requests something that is not supported by the
original CV, do not present it as fact.

Instead, identify it in the warnings section and leave it
out of the factual CV unless the original CV supports it.

CURRENT CV:
----------------
{cv_text}
----------------

TARGET JOB TITLE:
{target_job or "Not Provided"}

JOB DESCRIPTION:
{job_description or "Not Provided"}

USER INSTRUCTIONS:
{user_instructions or "No Additional Instructions"}

PREVIOUS CONVERSATION:
{conversation or "None"}

OBJECTIVES:

1. Create a complete ATS-friendly CV.

2. Preserve the candidate's factual experience.

3. Improve wording and professionalism.

4. Use strong action verbs.

5. Make achievements more impactful without changing their facts.

6. Preserve existing numbers and metrics.

7. Never fabricate numbers.

8. Never fabricate skills.

9. Never fabricate responsibilities.

10. Tailor the CV to the target role when provided.

11. Incorporate relevant keywords from the job description ONLY
    when supported by the candidate's actual experience.

12. Improve weak bullet points.

13. Remove unnecessary wording.

14. Avoid repetition.

15. Use standard ATS-friendly section names.

16. Keep the CV concise and professional.

17. Use plain text structure.

18. Do NOT use tables.

19. Do NOT use columns.

20. Do NOT use graphics.

21. Do NOT use icons.

22. Do NOT use emojis.

23. Do NOT use photos.

24. Do NOT add references unless the original CV contains them.

25. Do NOT add unsupported information.

26. If the user asks to add skills that are not present in the
    original CV, flag them for confirmation instead of presenting
    them as factual experience.

STRUCTURE:

Use a professional structure similar to:

NAME

CONTACT INFORMATION

PROFESSIONAL SUMMARY

CORE SKILLS

PROFESSIONAL EXPERIENCE

EDUCATION

CERTIFICATIONS

ADDITIONAL INFORMATION

Only include sections that are supported by the original CV.

BULLETS:

Use bullet points for responsibilities and achievements.

Prefer:

• Action + responsibility + result

when the information supports it.

Do not invent results.

IMPORTANT:

Return ONLY valid JSON.

Use exactly this structure:

{{
    "cv_text": "...",
    "summary": "...",
    "changes": [
        "...",
        "..."
    ],
    "warnings": [
        "..."
    ]
}}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        temperature=0.2,

        response_format={
            "type": "json_object"
        },

        messages=[

            {
                "role": "system",

                "content":
                    "You are an expert ATS CV optimization specialist. "
                    "Accuracy is more important than creativity."
            },

            {
                "role": "user",

                "content": prompt
            }

        ]

    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    data = json.loads(
        content
    )

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
        after_score -
        before_score
    )

    return result