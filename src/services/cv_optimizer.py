import re

from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# Helpers
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

    if isinstance(value, list):
        return value

    return []


def safe_int(value, default=0):

    try:
        return int(float(value))
    except Exception:
        return default


def clean_score(value):

    score = safe_int(value)

    return max(
        0,
        min(100, score)
    )


# ============================================================
# AI ATS Evaluation
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


    prompt = f"""
You are CareerAgent's professional ATS and recruitment evaluation engine.

Evaluate how ATS-friendly and relevant this CV is for the target role.

Do NOT simply count keywords.

Evaluate the actual quality and meaning of the CV.

Consider:

1. Relevance to the target role
2. Relevant keywords and terminology
3. Skills alignment
4. Professional summary quality
5. Experience relevance
6. Achievement orientation
7. Quantified achievements
8. Action-oriented language
9. Clear job titles
10. Standard CV sections
11. Readability
12. ATS-friendly structure
13. Education and certifications where relevant
14. Consistency
15. Overall recruiter searchability
16. Whether important job requirements are genuinely supported
17. Whether the CV contains unnecessary or irrelevant information

IMPORTANT:

Do not reward keyword stuffing.

Do not penalize the candidate merely because an exact keyword is absent
if equivalent experience is clearly demonstrated.

Do not assume a skill exists without evidence.

Do not invent information.

CV:
--------------------------------------------------
{cv_text}
--------------------------------------------------

TARGET JOB:
--------------------------------------------------
{target_job or "Not Provided"}
--------------------------------------------------

JOB DESCRIPTION:
--------------------------------------------------
{job_description or "Not Provided"}
--------------------------------------------------

Return ONLY valid JSON.

Use exactly:

{{
    "ats_score": 0,
    "relevance_score": 0,
    "keyword_score": 0,
    "structure_score": 0,
    "experience_score": 0,
    "achievement_score": 0,
    "readability_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_keywords": [],
    "supported_keywords": [],
    "improvement_suggestions": [],
    "overall_assessment": ""
}}

All scores must be integers from 0 to 100.

The final ats_score must represent your overall professional assessment.

Be realistic and selective.
"""


    system_prompt = """
You are CareerAgent's ATS evaluation engine.

Evaluate CVs professionally and objectively.

Never fabricate candidate information.

Do not use simplistic keyword counting.

Use semantic understanding.

Return valid JSON only.
"""


    try:

        response = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0.1,

            json_mode=True

        )


        data = extract_json(
            response
        )


        if not isinstance(
            data,
            dict
        ):

            return 0


        return clean_score(
            data.get(
                "ats_score",
                0
            )
        )


    except Exception as e:

        print(
            "AI ATS evaluation error:",
            e
        )

        return 0


# ============================================================
# Detailed AI ATS Evaluation
# ============================================================

def evaluate_ats_with_ai(
    cv_text,
    target_job="",
    job_description=""
):

    prompt = f"""
You are CareerAgent's senior ATS and recruitment evaluator.

Perform a detailed evaluation of this CV against the target job.

Evaluate the candidate based on real evidence.

Never invent experience.

Consider semantic equivalents rather than exact keyword matching.

Evaluate:

- Job relevance
- Skills
- Experience
- Seniority
- Responsibilities
- Achievements
- Quantification
- Keywords
- ATS structure
- Readability
- Professional summary
- Core skills
- Experience bullets
- Education
- Certifications
- Overall recruiter appeal

Identify:

- Strong areas
- Weak areas
- Supported job keywords
- Important missing keywords
- Concrete CV improvements

IMPORTANT:

A missing keyword should only be recommended when the candidate's
existing experience reasonably supports using it.

Do not recommend falsely claiming skills.

CV:
--------------------------------------------------
{cv_text}
--------------------------------------------------

TARGET JOB:
--------------------------------------------------
{target_job or "Not Provided"}
--------------------------------------------------

JOB DESCRIPTION:
--------------------------------------------------
{job_description or "Not Provided"}
--------------------------------------------------

Return ONLY JSON:

{{
    "ats_score": 0,
    "relevance_score": 0,
    "keyword_score": 0,
    "structure_score": 0,
    "experience_score": 0,
    "achievement_score": 0,
    "readability_score": 0,

    "strengths": [],

    "weaknesses": [],

    "missing_keywords": [],

    "supported_keywords": [],

    "improvement_suggestions": [],

    "overall_assessment": ""
}}

All scores must be integers from 0 to 100.
"""


    system_prompt = """
You are CareerAgent's professional ATS intelligence engine.

Accuracy is more important than generosity.

Never fabricate candidate experience.

Never recommend falsely claiming a skill.

Return valid JSON only.
"""


    try:

        response = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0.1,

            json_mode=True

        )


        data = extract_json(
            response
        )


        if not isinstance(
            data,
            dict
        ):

            return {}


        return data


    except Exception as e:

        print(
            "AI ATS detailed evaluation error:",
            e
        )

        return {}


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
You are CareerAgent's expert CV writer, recruiter and ATS optimization
specialist.

Your task is to improve the candidate's CV for the target role.

FACTUAL RULES:

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

You may use terminology from the job description ONLY when the
candidate's existing experience supports that terminology.

If the user requests something unsupported by the CV, do not add it
as fact.

Instead, mention it in warnings.

CURRENT CV:
--------------------------------------------------
{cv_text}
--------------------------------------------------

TARGET JOB:
--------------------------------------------------
{target_job or "Not Provided"}
--------------------------------------------------

JOB DESCRIPTION:
--------------------------------------------------
{job_description or "Not Provided"}
--------------------------------------------------

USER INSTRUCTIONS:
--------------------------------------------------
{user_instructions or "No Additional Instructions"}
--------------------------------------------------

PREVIOUS CONVERSATION:
--------------------------------------------------
{conversation or "None"}
--------------------------------------------------


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
11. Use relevant supported job-description terminology.
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

Use exactly:

{{
    "cv_text": "FULL UPDATED CV HERE",
    "summary": "SHORT DESCRIPTION OF WHAT WAS IMPROVED",
    "changes": [],
    "warnings": []
}}
"""


    system_prompt = """
You are CareerAgent's CV optimization engine.

Accuracy is more important than creativity.

Never fabricate candidate information.

Return valid JSON only.

Do not include markdown outside the JSON.
"""


    try:

        content = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0.1,

            json_mode=True

        )


        data = extract_json(
            content
        )


    except Exception as e:

        print(
            "AI CV generation error:",
            e
        )

        return {

            "cv_text": cv_text,

            "summary": "",

            "changes": [],

            "warnings": [
                "AI CV optimization could not be completed."
            ]

        }


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
# Full AI CV Optimization
# ============================================================

def optimize_cv(
    cv_text,
    target_job="",
    job_description="",
    user_instructions="",
    conversation=""
):

    print(
        "Running AI ATS evaluation before optimization..."
    )


    before_evaluation = evaluate_ats_with_ai(

        cv_text,

        target_job,

        job_description

    )


    before_score = clean_score(

        before_evaluation.get(
            "ats_score",
            0
        )

    )


    print(
        f"AI ATS score before optimization: {before_score}"
    )


    # ========================================================
    # Generate Optimized CV
    # ========================================================

    result = generate_cv(

        cv_text,

        target_job,

        job_description,

        user_instructions,

        conversation

    )


    # ========================================================
    # Evaluate Optimized CV
    # ========================================================

    print(
        "Running AI ATS evaluation after optimization..."
    )


    after_evaluation = evaluate_ats_with_ai(

        result["cv_text"],

        target_job,

        job_description

    )


    after_score = clean_score(

        after_evaluation.get(
            "ats_score",
            0
        )

    )


    print(
        f"AI ATS score after optimization: {after_score}"
    )


    # ========================================================
    # Attach AI Evaluation
    # ========================================================

    result["before_score"] = (
        before_score
    )

    result["after_score"] = (
        after_score
    )

    result["score_change"] = (

        after_score
        -
        before_score

    )


    result["before_evaluation"] = (
        before_evaluation
    )

    result["after_evaluation"] = (
        after_evaluation
    )


    return result