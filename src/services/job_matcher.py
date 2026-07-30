import re
import time
import traceback

from src.services.llm import (
    ask_ollama,
    extract_json
)


# ============================================================
# CONFIGURATION
# ============================================================

AI_BATCH_SIZE = 10

AI_RETRY_ATTEMPTS = 2

AI_RETRY_DELAY = 2


# ============================================================
# PYTHON SKILL DATABASE
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
# HELPERS
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

        return int(
            float(value)
        )

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
# PYTHON SKILL EXTRACTION
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

            found.append(
                skill
            )

    return found


# ============================================================
# PYTHON SKILL MATCHING
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

        "cv_skills":
            cv_skills,

        "job_skills":
            job_skills,

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "transferable_skills":
            transferable
    }


# ============================================================
# PYTHON CV ENHANCEMENT
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
# PREPARE PYTHON ANALYSIS
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
# PREPARE COMPACT JOB DATA FOR AI
# ============================================================

def prepare_ai_jobs(jobs):

    ai_jobs = []

    for index, job in enumerate(jobs):

        description = str(
            job.get(
                "description",
                ""
            )
        )

        # Keep prompt size controlled
        description = description[:3500]

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
# BUILD AI PROMPT
# ============================================================

def build_ai_prompt(
    cv_text,
    ai_jobs
):

    return f"""
You are CareerAgent's recruitment matching engine.

Evaluate EVERY job in this batch against the candidate's CV.

IMPORTANT RULES:

1. Analyze every single job.
2. Return exactly one result for every job.
3. Keep the original job index.
4. Never invent experience.
5. Do not assume a skill simply because it is common in the industry.
6. Use semantic understanding, not just keyword matching.
7. Consider the candidate's actual career progression.
8. Consider transferable experience.
9. Consider job title relevance.
10. Consider seniority.
11. Consider actual responsibilities.
12. Consider technical requirements.
13. Consider industry relevance.
14. Consider leadership requirements.
15. Consider overall career suitability.

Python has already calculated:

- matched_skills
- missing_skills
- transferable_skills

Use these as supporting information.

Do NOT simply count keywords.

The final match score should represent the REALISTIC probability that this candidate is a strong applicant for the role.

--------------------------------------------------
CANDIDATE CV
--------------------------------------------------

{cv_text}

--------------------------------------------------
JOBS
--------------------------------------------------

{ai_jobs}

--------------------------------------------------
RETURN JSON ONLY
--------------------------------------------------

Return exactly this structure:

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

--------------------------------------------------
SCORING
--------------------------------------------------

90-100 = Exceptional fit
80-89  = Excellent fit
70-79  = Good fit
60-69  = Moderate fit
50-59  = Partial fit
0-49   = Weak fit

match_level MUST be exactly one of:

"Exceptional fit"
"Excellent fit"
"Good fit"
"Moderate fit"
"Partial fit"
"Weak fit"

All scores must be integers from 0 to 100.

Keep explanations concise.

Return valid JSON only.
"""


# ============================================================
# VALIDATE AI RESULT
# ============================================================

def validate_ai_results(
    results,
    job_count
):

    if not isinstance(
        results,
        list
    ):

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

        if index >= job_count:
            continue

        # Clean numeric values
        item["match_score"] = clean_score(
            item.get(
                "match_score",
                0
            )
        )

        item["title_match"] = clean_score(
            item.get(
                "title_match",
                0
            )
        )

        item["seniority_match"] = clean_score(
            item.get(
                "seniority_match",
                0
            )
        )

        item["industry_match"] = clean_score(
            item.get(
                "industry_match",
                0
            )
        )

        item["experience_match"] = clean_score(
            item.get(
                "experience_match",
                0
            )
        )

        item["technical_match"] = clean_score(
            item.get(
                "technical_match",
                0
            )
        )

        item["leadership_match"] = clean_score(
            item.get(
                "leadership_match",
                0
            )
        )

        item["strengths"] = safe_list(
            item.get(
                "strengths",
                []
            )
        )

        item["gaps"] = safe_list(
            item.get(
                "gaps",
                []
            )
        )

        analysis_map[index] = item

    return analysis_map


# ============================================================
# ANALYZE ONE AI BATCH
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

    prompt = build_ai_prompt(
        cv_text,
        ai_jobs
    )

    system_prompt = """
You are CareerAgent's recruitment matching engine.

Your job is to evaluate candidate-job fit accurately.

Accuracy is more important than generosity.

Never fabricate candidate experience.

Analyze every job.

Return valid JSON only.
"""

    for attempt in range(
        1,
        AI_RETRY_ATTEMPTS + 1
    ):

        try:

            print(
                f"AI analyzing batch of {len(jobs)} jobs "
                f"(attempt {attempt}/{AI_RETRY_ATTEMPTS})..."
            )

            response = ask_ollama(

                prompt,

                system_prompt=system_prompt,

                temperature=0.1,

                json_mode=True,

                timeout=120

            )

            if not response:

                raise RuntimeError(
                    "AI returned an empty response."
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

                raise RuntimeError(
                    "AI response was not a JSON object."
                )

            results = data.get(
                "results",
                []
            )

            analysis_map = validate_ai_results(

                results,

                len(jobs)

            )

            print(
                f"Valid AI results: "
                f"{len(analysis_map)}/{len(jobs)}"
            )

            # ------------------------------------------------
            # Success
            # ------------------------------------------------

            if len(analysis_map) == len(jobs):

                return analysis_map

            # ------------------------------------------------
            # Partial response
            # ------------------------------------------------

            if analysis_map:

                print(
                    "AI returned only partial results."
                )

                # Retry to try to complete the batch
                if attempt < AI_RETRY_ATTEMPTS:

                    time.sleep(
                        AI_RETRY_DELAY
                    )

                    continue

                return analysis_map

            raise RuntimeError(
                "AI returned no valid job analyses."
            )

        except Exception as e:

            print(
                "AI batch failed:"
            )

            print(
                repr(e)
            )

            if attempt < AI_RETRY_ATTEMPTS:

                print(
                    f"Retrying in "
                    f"{AI_RETRY_DELAY} seconds..."
                )

                time.sleep(
                    AI_RETRY_DELAY
                )

            else:

                traceback.print_exc()

    return {}


# ============================================================
# ANALYZE ALL JOBS IN BATCHES
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

    total_batches = (
        total_jobs
        +
        AI_BATCH_SIZE
        -
        1
    ) // AI_BATCH_SIZE

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
        f"Expected batches: {total_batches}"
    )

    print(
        "=================================================="
    )

    analysis_map = {}

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
            batch_start
            //
            AI_BATCH_SIZE
        ) + 1

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

        local_analysis = (
            analyze_job_batch_with_ai(
                cv_text,
                batch
            )
        )

        if not local_analysis:

            print(
                f"Batch {batch_number} "
                "returned no AI results."
            )

            continue

        # ----------------------------------------------------
        # Convert local index to global index
        # ----------------------------------------------------

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
# PYTHON FALLBACK SCORE
# ============================================================

def calculate_python_fallback_score(
    job
):

    matched = len(
        job.get(
            "matched_skills",
            []
        )
    )

    missing = len(
        job.get(
            "missing_skills",
            []
        )
    )

    transferable = len(
        job.get(
            "transferable_skills",
            []
        )
    )

    total = (
        matched
        +
        missing
    )

    if total <= 0:

        return 40

    direct_ratio = (
        matched
        /
        total
    )

    score = (
        direct_ratio
        *
        80
    )

    bonus = min(
        transferable * 5,
        20
    )

    score = score + bonus

    return clean_score(
        score
    )


# ============================================================
# APPLY AI RESULT
# ============================================================

def apply_ai_analysis(
    job,
    analysis
):

    # ========================================================
    # AI UNAVAILABLE
    # ========================================================

    if not analysis:

        fallback_score = (
            calculate_python_fallback_score(
                job
            )
        )

        job["match_score"] = (
            fallback_score
        )

        job["title_score"] = 0

        job["seniority_score"] = 0

        job["industry_score"] = 0

        job["experience_score"] = 0

        job["technical_score"] = 0

        job["leadership_score"] = 0

        # ----------------------------------------------------
        # Important:
        # Do NOT pretend this is an AI score.
        # ----------------------------------------------------

        job["match_level"] = (
            "Python Match"
        )

        job["match_reason"] = (
            "AI analysis was unavailable. "
            "This score is based on Python skill matching "
            "and transferable skills only."
        )

        job["ai_ranking_reason"] = ""

        job["strengths"] = (
            job.get(
                "matched_skills",
                []
            )
        )

        job["gaps"] = (
            job.get(
                "missing_skills",
                []
            )
        )

        job["recommendation"] = (
            job.get(
                "cv_enhancement",
                ""
            )
        )

        job["ai_analyzed"] = False

        return job

    # ========================================================
    # AI RESULT AVAILABLE
    # ========================================================

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
# MAIN JOB MATCHING
# ============================================================

def match_jobs(
    cv_text,
    jobs
):

    if not jobs:

        return []

    # --------------------------------------------------------
    # No CV
    # --------------------------------------------------------

    if not cv_text:

        print(
            "No CV provided. "
            "Skipping job matching."
        )

        return jobs

    # ========================================================
    # STEP 1
    # Python skill analysis
    # ========================================================

    jobs = prepare_python_analysis(

        cv_text,

        jobs

    )

    # ========================================================
    # STEP 2
    # AI batch analysis
    # ========================================================

    analysis_map = (
        analyze_all_jobs_with_ai(

            cv_text,

            jobs

        )
    )

    # ========================================================
    # STEP 3
    # Apply AI / fallback analysis
    # ========================================================

    for index, job in enumerate(
        jobs
    ):

        analysis = (
            analysis_map.get(
                index
            )
        )

        apply_ai_analysis(

            job,

            analysis

        )

    # ========================================================
    # STEP 4
    # Sort by match score
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
    # Assign rank AFTER sorting
    # ========================================================

    for rank, job in enumerate(

        jobs,

        start=1

    ):

        job["rank"] = rank

    # ========================================================
    # FINAL STATISTICS
    # ========================================================

    analyzed_count = len([

        job

        for job in jobs

        if job.get(
            "ai_analyzed",
            False
        )

    ])

    unavailable_count = (
        len(jobs)
        -
        analyzed_count
    )

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