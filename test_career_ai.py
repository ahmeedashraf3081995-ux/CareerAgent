from src.services.cv_analyzer import analyze_cv
from src.services.job_matcher import match_jobs


cv = """
Ahmed Abdelbary

Assistant Manager - Demand & Supply Planning
Samsung

Experienced supply chain and demand planning professional
with experience across MENA and GCC.

Skills:
Demand Planning
Supply Planning
Inventory Optimization
Forecasting
SAP
Power BI
Tableau
Excel
Python

Experience:
Managing demand and supply planning activities.
Working with sales teams and regional branches.
Forecasting demand and monitoring inventory.
Using SAP, Excel, Power BI and Tableau for analysis.
"""


job = {
    "job_title": "Senior Demand Planning Manager",
    "company": "Test Company",
    "location": "Dubai",
    "description": """
    We are looking for a Senior Demand Planning Manager.

    Requirements:
    - Demand planning experience
    - Forecasting
    - Inventory optimization
    - SAP
    - Power BI
    - Strong analytical skills
    - Experience working with regional teams
    """
}


print("\n==============================")
print("TEST 1: CV ANALYZER")
print("==============================")

cv_analysis = analyze_cv(cv)

print(cv_analysis)


print("\n==============================")
print("TEST 2: AI JOB MATCHING")
print("==============================")

results = match_jobs(
    cv,
    [job]
)

print(results[0])


print("\n==============================")
print("TEST COMPLETED")
print("==============================")