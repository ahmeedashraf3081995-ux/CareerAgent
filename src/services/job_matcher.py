import re

from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# Configuration
# ============================================================

AI_BATCH_SIZE = 10


# ============================================================
# Python Skill Database
# ============================================================

SKILL_GROUPS = {

    "Demand Planning": [
        "demand planning",
        "demand planner",
        "demand forecasting",
        "demand forecast",
        "forecasting",
        "forecast",
    ],

    "Supply Planning": [
        "supply planning",
        "supply planner",
        "supply chain planning",
    ],

    "Inventory Optimization": [
        "inventory optimization",
        "inventory management",
        "inventory planning",
        "stock optimization",
        "stock management",
        "stock availability",
        "inventory control",
    ],

    "S&OP": [
        "s&op",
        "sales and operations planning",
        "sales & operations planning",
    ],

    "Forecasting": [
        "forecasting",
        "forecast",
        "forecast accuracy",
        "forecast error",
        "demand forecast",
    ],

    "SAP": [
        "sap",
    ],

    "Power BI": [
        "power bi",
        "powerbi",
    ],

    "Tableau": [
        "tableau",
    ],

    "Excel": [
        "excel",
        "microsoft excel",
    ],

    "Python": [
        "python",
    ],

    "Oracle": [
        "oracle",
    ],

    "SQL": [
        "sql",
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics",
        "analytical skills",
        "analytics",
    ],

    "Supply Chain": [
        "supply chain",
        "supply chain management",
    ],

    "Merchandising": [
        "merchandising",
        "merchandise planning",
        "merchandise planner",
    ],

    "OTB": [
        "open-to-buy",
        "open to buy",
        "otb",
    ],

    "S&DP": [
        "s&dp",
        "sales and distribution planning",
        "sales and demand planning",
    ],

    "Cross-functional Collaboration": [
        "cross-functional",
        "cross functional",
        "cross-functional teams",
        "cross functional teams",
        "stakeholder management",
        "stakeholder collaboration",
    ],

    "Regional Planning": [
        "regional planning",
        "regional teams",
        "regional team",
        "mena",
        "gcc",
    ],

    "Leadership": [
        "leadership",
        "team management",
        "people management",
        "managed a team",
        "manage a team",
        "led a team",
        "team lead",
    ],

    "Project Management": [
        "project management",
        "project manager",
        "managed projects",
        "project planning",
    ],

    "Process Improvement": [
        "process improvement",
        "continuous improvement",
        "process optimization",
        "automation",
    ],
}


# ============================================================
# Helpers
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def contains_skill(text, keywords):

    text = normalize_text(text)

    for keyword in keywords:

        keyword = normalize_text(keyword)

        if not keyword:
            continue

        if len(keyword) <= 4:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text
            ):
                return True

        else:

            if keyword in text:
                return True

    return False


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
        min(
            100,
            score
        )
    )


# ============================================================
# Python Skill Extraction
# ============================================================

def extract_python_skills(text):

    found = []

    text = normalize_text(text)

    if not text:
        return found

    for skill, keywords in SKILL_GROUPS.items():

        if contains_skill(
            text,
            keywords
        ):

            found.append(skill)

    return found


# ============================================================
# Python Skill Matching
# ============================================================

def calculate_skill_matching(
    cv_text,
    job_description
):

    cv_skills = extract_python_skills(
        cv_text
    )

    job_skills = extract_python_skills(
        job_description
    )

    matched = []

    missing = []

    for skill in job_skills:

        if skill in cv_skills:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    # --------------------------------------------------------
    # Transferable Skills
    # --------------------------------------------------------

    transferable = []

    transferable_map = {

        "Demand Planning": [
            "Supply Planning",
            "Forecasting",
            "Inventory Optimization"
        ],

        "Supply Planning": [
            "Demand Planning",
            "Inventory Optimization"
        ],

        "Inventory Optimization": [
            "Demand Planning",
            "Supply Planning"
        ],

        "Forecasting": [
            "Demand Planning",
            "Data Analysis"
        ],

        "Power BI": [
            "Tableau",
            "Data Analysis"
        ],

        "Tableau": [
            "Power BI",
            "Data Analysis"
        ],

        "Excel": [
            "Data Analysis"
        ],

        "Supply Chain": [
            "Demand Planning",
            "Supply Planning",
            "Inventory Optimization"
        ],

        "Merchandising": [
            "Demand Planning",
            "Inventory Optimization",
            "OTB"
        ],

        "Regional Planning": [
            "Cross-functional Collaboration",
            "Supply Chain"
        ],
    }

    for missing_skill in missing:

        alternatives = transferable_map.get(
            missing_skill,
            []
        )

        for alternative in alternatives:

            if alternative in cv_skills:

                if alternative not in transferable:

                    transferable.append(
                        alternative
                    )

    return {

        "cv_skills": cv_skills,

        "job_skills": job_skills,

        "matched_skills": matched,

        "missing_skills": missing,

        "transferable_skills": transferable
    }


# ============================================================
# Python CV Enhancement
# ============================================================

def generate_cv_enhancement(
    cv_text,
    matched_skills,
    missing_skills,
    transferable_skills
):

    if not matched_skills:

        if missing_skills:

            return (
                "Your CV has limited direct alignment with "
                "this role. Highlight any genuine relevant "
                "experience related to the missing requirements."
            )

        return (
            "Review the job requirements and emphasize "
            "the most relevant experience from your CV."
        )

    priority = [

        "Demand Planning",
        "Supply Planning",
        "Inventory Optimization",
        "Forecasting",
        "S&OP",
        "SAP",
        "Power BI",
        "Tableau",
        "Excel",
        "Data Analysis",
        "Supply Chain",
        "Regional Planning",
        "Cross-functional Collaboration",
        "Leadership",
        "Process Improvement"
    ]

    selected = []

    for skill in priority:

        if skill in matched_skills:

            selected.append(
                skill
            )

        if len(selected) >= 4:
            break

    if selected:

        skill_text = ", ".join(
            selected
        )

        message = (
            "Emphasize your "
            + skill_text
            + " experience in the CV, "
            "preferably with measurable business impact."
        )

    else:

        message = (
            "Emphasize the most relevant responsibilities "
            "and measurable achievements from your CV."
        )

    if transferable_skills:

        transfer_text = ", ".join(
            transferable_skills[:2]
        )

        message += (
            f" Also highlight your {transfer_text} "
            "experience where relevant."
        )

    if missing_skills:

        missing_text = ", ".join(
            missing_skills[:2]
        )

        message += (
            f" If you have genuine exposure to "
            f"{missing_text}, make it more visible."
        )

    return message


# ============================================================
# Prepare Python Analysis
# ============================================================

def prepare_python_analysis(
    cv_text,
    jobs
):

    print(
        f"Python analyzing {len(jobs)} jobs..."
    )

    for job in jobs:

        description = job.get(
            "description",
            ""
        )

        skill_analysis = calculate_skill_matching(

            cv_text,

            (
                job.get(
                    "job_title",
                    ""
                )
                + " "
                + description
            )

        )

        job["matched_skills"] = (
            skill_analysis["matched_skills"]
        )

        job["missing_skills"] = (
            skill_analysis["missing_skills"]
        )

        job["transferable_skills"] = (
            skill_analysis["transferable_skills"]
        )

        job["cv_enhancement"] = (
            generate_cv_enhancement(

                cv_text,

                job["matched_skills"],

                job["missing_skills"],

                job["transferable_skills"]

            )
        )

    print(
        "Python job analysis completed."
    )

    return jobs


# ============================================================
# Compact Job Data For AI
# ============================================================

def prepare_ai_jobs(jobs):

    ai_jobs = []

    for index, job in enumerate(jobs):

        description = str(
            job.get(
                "description",
                ""
            )
        )[:3000]

        ai_jobs.append({

            "index":
                index,

            "title":
                job.get(
                    "job_title",
                    ""
                ),

            "company":
                job.get(
                    "company",
                    ""
                ),

            "location":
                job.get(
                    "location",
                    ""
                ),

            "description":
                description,

            "matched_skills":
                job.get(
                    "matched_skills",
                    []
                ),

            "missing_skills":
                job.get(
                    "missing_skills",
                    []
                ),

            "transferable_skills":
                job.get(
                    "transferable_skills",
                    []
                )

        })

    return ai_jobs


# ============================================================
# Analyze ONE AI Batch
# ============================================================

def analyze_job_batch_with_ai(
    cv_text,
    jobs
):

    if not jobs:

        return {}


    ai_jobs = prepare_ai_jobs(
        jobs
    )


    prompt = f"""
You are CareerAgent's recruitment matching engine.

Evaluate ALL jobs in this batch against the candidate's CV.

IMPORTANT:

This is a batch analysis.

You MUST analyze every job.

Do NOT skip jobs.

Do NOT invent experience.

Use semantic understanding rather than simple keyword matching.

Consider:

- Actual candidate experience
- Responsibilities
- Career progression
- Seniority
- Job title
- Industry
- Technical background
- Leadership
- Planning experience
- Job responsibilities
- Job requirements
- Overall career suitability

Python has already calculated:

- matched skills
- missing skills
- transferable skills

Do NOT recalculate those.

Your job is to judge the overall career fit.

--------------------------------------------------
CANDIDATE CV
--------------------------------------------------

{cv_text}

--------------------------------------------------
JOBS IN THIS BATCH
--------------------------------------------------

{ai_jobs}

--------------------------------------------------
RETURN JSON ONLY
--------------------------------------------------

Return exactly:

{{
    "results": [
        {{
            "index": 0,
            "match_score": 0,
            "match_level": "",
            "title_match": 0,
            "seniority_match": 0,
            "industry_match": 0,
            "experience_match": 0,
            "technical_match": 0,
            "leadership_match": 0,
            "ranking_reason": "",
            "match_reason": "",
            "strengths": [],
            "gaps": [],
            "recommendation": ""
        }}
    ]
}}

RULES:

- Return ONE result for EVERY job in this batch.
- Keep the original index.
- Never invent experience.
- All scores must be integers from 0 to 100.
- Keep explanations concise.

match_level must be one of:

"Exceptional fit"
"Excellent fit"
"Good fit"
"Moderate fit"
"Partial fit"
"Weak fit"

Scoring:

90-100 = Exceptional fit
80-89 = Excellent fit
70-79 = Good fit
60-69 = Moderate fit
50-59 = Partial fit
0-49 = Weak fit

Return valid JSON only.
"""


    system_prompt = """
You are CareerAgent's recruitment matching engine.

Analyze every job in the provided batch.

Accuracy is more important than generosity.

Never fabricate candidate experience.

Return valid JSON only.
"""


    try:

        print(
            f"AI analyzing batch of {len(jobs)} jobs..."
        )


        response = ask_ollama(

            prompt,

            system_prompt=system_prompt,

            temperature=0.1,

            json_mode=True

        )


        print(
            "AI batch response received."
        )


        data = extract_json(
            response
        )


        if not isinstance(
            data,
            dict
        ):

            print(
                "AI batch response was not a JSON object."
            )

            return {}


        results = data.get(
            "results",
            []
        )


        if not isinstance(
            results,
            list
        ):

            print(
                "AI batch JSON did not contain a valid results list."
            )

            return {}


        analysis_map = {}


        for item in results:

            if not isinstance(
                item,
                dict
            ):
                continue


            try:

                index = int(
                    item.get(
                        "index",
                        -1
                    )
                )

            except Exception:

                continue


            if index < 0:

                continue


            analysis_map[index] = item


        print(
            f"Batch AI results: "
            f"{len(analysis_map)}/{len(jobs)}"
        )


        return analysis_map


    except Exception as e:

        import traceback


        print(
            "AI batch failed:"
        )

        print(
            repr(e)
        )


        traceback.print_exc()


        return {}


# ============================================================
# Analyze ALL Jobs In Batches
# ============================================================

def analyze_all_jobs_with_ai(
    cv_text,
    jobs
):

    if not jobs:

        return {}


    total_jobs = len(
        jobs
    )


    print(
        "=================================================="
    )

    print(
        f"Starting AI batch analysis: "
        f"{total_jobs} jobs"
    )

    print(
        f"Batch size: {AI_BATCH_SIZE}"
    )

    print(
        f"Expected batches: "
        f"{(total_jobs + AI_BATCH_SIZE - 1) // AI_BATCH_SIZE}"
    )

    print(
        "=================================================="
    )


    analysis_map = {}


    # ========================================================
    # Split Jobs Into Small Batches
    # ========================================================

    for batch_start in range(
        0,
        total_jobs,
        AI_BATCH_SIZE
    ):

        batch_end = min(

            batch_start
            +
            AI_BATCH_SIZE,

            total_jobs

        )


        batch = jobs[
            batch_start:batch_end
        ]


        batch_number = (
            batch_start // AI_BATCH_SIZE
        ) + 1


        total_batches = (
            total_jobs
            +
            AI_BATCH_SIZE
            -
            1
        ) // AI_BATCH_SIZE


        print(
            ""
        )

        print(
            "--------------------------------------------------"
        )

        print(
            f"AI BATCH {batch_number}/{total_batches}"
        )

        print(
            f"Jobs {batch_start + 1} "
            f"to {batch_end}"
        )

        print(
            "--------------------------------------------------"
        )


        # ====================================================
        # Convert Local Batch Index To Global Index
        # ====================================================

        local_analysis = (
            analyze_job_batch_with_ai(
                cv_text,
                batch
            )
        )


        # ====================================================
        # Map Results Back To Original Job Index
        # ====================================================

        for local_index, analysis in (
            local_analysis.items()
        ):

            if not isinstance(
                local_index,
                int
            ):
                continue


            if local_index < 0:

                continue


            if local_index >= len(
                batch
            ):

                continue


            global_index = (
                batch_start
                +
                local_index
            )


            analysis_map[
                global_index
            ] = analysis


    # ========================================================
    # Final Statistics
    # ========================================================

    print(
        ""
    )

    print(
        "=================================================="
    )

    print(
        f"AI analysis completed: "
        f"{len(analysis_map)}/{total_jobs} jobs"
    )

    print(
        "=================================================="
    )


    return analysis_map


# ============================================================
# Apply AI Result To Job
# ============================================================

def apply_ai_analysis(
    job,
    analysis
):

    if not analysis:

        job["match_score"] = 0

        job["title_score"] = 0

        job["seniority_score"] = 0

        job["industry_score"] = 0

        job["experience_score"] = 0

        job["technical_score"] = 0

        job["leadership_score"] = 0

        job["match_level"] = (
            "AI Analysis Unavailable"
        )

        job["match_reason"] = (
            "The AI matching service was "
            "temporarily unavailable for this job. "
            "Python skill matching is still available."
        )

        job["ai_ranking_reason"] = ""

        job["strengths"] = []

        job["gaps"] = []

        job["recommendation"] = ""

        job["ai_analyzed"] = False

        return job


    job["match_score"] = clean_score(
        analysis.get(
            "match_score",
            0
        )
    )


    job["title_score"] = clean_score(
        analysis.get(
            "title_match",
            0
        )
    )


    job["seniority_score"] = clean_score(
        analysis.get(
            "seniority_match",
            0
        )
    )


    job["industry_score"] = clean_score(
        analysis.get(
            "industry_match",
            0
        )
    )


    job["experience_score"] = clean_score(
        analysis.get(
            "experience_match",
            0
        )
    )


    job["technical_score"] = clean_score(
        analysis.get(
            "technical_match",
            0
        )
    )


    job["leadership_score"] = clean_score(
        analysis.get(
            "leadership_match",
            0
        )
    )


    job["match_level"] = (

        analysis.get(
            "match_level",
            ""
        )

        or

        "AI Match"

    )


    job["match_reason"] = (

        analysis.get(
            "match_reason",
            ""
        )

        or

        analysis.get(
            "ranking_reason",
            ""
        )

    )


    job["ai_ranking_reason"] = (

        analysis.get(
            "ranking_reason",
            ""
        )

    )


    job["strengths"] = safe_list(
        analysis.get(
            "strengths",
            []
        )
    )


    job["gaps"] = safe_list(
        analysis.get(
            "gaps",
            []
        )
    )


    job["recommendation"] = (

        analysis.get(
            "recommendation",
            ""
        )

    )


    job["ai_analyzed"] = True


    return job


# ============================================================
# Main Job Matching
# ============================================================

def match_jobs(
    cv_text,
    jobs
):

    if not cv_text:

        return jobs or []


    if not jobs:

        return []


    # ========================================================
    # STEP 1
    # Python handles ALL jobs
    # ========================================================

    jobs = prepare_python_analysis(

        cv_text,

        jobs

    )


    # ========================================================
    # STEP 2
    # AI handles jobs in batches
    # ========================================================

    analysis_map = analyze_all_jobs_with_ai(

        cv_text,

        jobs

    )


    # ========================================================
    # STEP 3
    # Apply AI results
    # ========================================================

    for index, job in enumerate(
        jobs
    ):

        analysis = analysis_map.get(
            index
        )


        apply_ai_analysis(

            job,

            analysis

        )


    # ========================================================
    # STEP 4
    # Sort By Match Score
    # ========================================================

    jobs.sort(

        key=lambda x: x.get(
            "match_score",
            0
        ),

        reverse=True

    )


    # ========================================================
    # STEP 5
    # Rank
    # ========================================================

    for rank, job in enumerate(

        jobs,

        start=1

    ):

        job["rank"] = rank


    # ========================================================
    # Final Statistics
    # ========================================================

    analyzed_count = len([

        job

        for job in jobs

        if job.get(
            "ai_analyzed",
            False
        )

    ])


    unavailable_count = len(
        jobs
    ) - analyzed_count


    print(
        ""
    )

    print(
        "=================================================="
    )

    print(
        "AI JOB MATCHING COMPLETED"
    )

    print(
        f"Total jobs: {len(jobs)}"
    )

    print(
        f"AI analyzed: {analyzed_count}"
    )

    print(
        f"AI unavailable: {unavailable_count}"
    )

    print(
        "=================================================="
    )


    return jobs