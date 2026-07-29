import json


def load_profile(profile_path='data/profile/user_profile.json'):
    """Load user profile from JSON file."""
    with open(profile_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def clean_salary(value):
    """Convert salary values like 'AED 24,500' into numbers."""
    if value is None:
        return None

    try:
        return float(
            str(value)
            .replace(',', '')
            .replace('AED', '')
            .strip()
        )
    except ValueError:
        return None


def calculate_similarity(job, user):
    """
    Calculate job match score.
    Current scoring:
    - Title match: 30 points
    - Skills match: up to 30 points
    - Industry match: 10 points
    - Experience match: 15 points
    - Location match: 10 points
    - Salary match: 5 points
    """

    score = 0

    # Title matching
    job_title = job.get('title', '').lower()
    user_role = user.get('current_role', '').lower()

    title_keywords = [
        word for word in job_title.split()
        if len(word) > 3
    ]

    if any(keyword in user_role for keyword in title_keywords):
        score += 30


    # Skills matching
    job_skills = set(job.get('skills', []))
    user_skills = set(user.get('core_skills', []))

    common_skills = job_skills.intersection(user_skills)

    score += min(len(common_skills) * 10, 30)


    # Industry matching
    job_industry = job.get('industry', '').lower()
    user_industry = str(user.get('industry_preference', '')).lower()

    if job_industry and job_industry in user_industry:
        score += 10


    # Experience matching
    user_experience = user.get('experience', 0)
    required_experience = job.get('min_years_experience', 0)

    if user_experience >= required_experience:
        score += 15


    # Location matching
    job_locations = [
        location.lower()
        for location in job.get('target_locations', [])
    ]

    user_location = str(
        user.get('current_location', '')
    ).lower()

    if any(user_location in location for location in job_locations):
        score += 10


    # Salary matching
    job_salary = clean_salary(job.get('salary_per_month'))
    user_salary = clean_salary(user.get('current_uae_salary'))

    if job_salary and user_salary:
        if job_salary >= user_salary:
            score += 5


    return min(score, 100), common_skills


def generate_recommendation(score):
    """Generate application recommendation."""

    if score >= 85:
        return "APPLY"
    elif score >= 65:
        return "REVIEW"
    else:
        return "SKIP"


def job_matcher(job, profile_path='data/profile/user_profile.json'):
    """Match a job against user profile."""

    user = load_profile(profile_path)

    score, matched_skills = calculate_similarity(job, user)

    missing_skills = list(
        set(job.get('skills', []))
        -
        set(user.get('core_skills', []))
    )

    return {
        "overall_score": score,
        "matched_skills": list(matched_skills),
        "missing_skills": missing_skills,
        "recommendation": generate_recommendation(score)
    }


# Test job
if __name__ == "__main__":

    job_posting = {
        "title": "Senior Demand Planner",
        "industry": "Technology",
        "skills": [
            "Demand Forecasting",
            "S&OP",
            "Inventory Optimization"
        ],
        "min_years_experience": 5,
        "target_locations": [
            "Canada",
            "UAE"
        ],
        "salary_per_month": "AED 24,500"
    }

    result = job_matcher(job_posting)

    print(json.dumps(result, indent=4))