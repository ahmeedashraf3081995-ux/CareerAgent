def generate_profile(cv_text):

    text = cv_text.lower()

    profile = {
        "job_titles": [],
        "countries": ["UAE"],
        "cities": ["Dubai"],
        "companies": [],
        "keywords": []
    }


    # Job title detection

    roles = {
        "Demand Planner": [
            "demand planning",
            "forecasting",
            "demand planner"
        ],

        "Supply Planner": [
            "supply planning",
            "supply planner"
        ],

        "Supply Chain Analyst": [
            "supply chain",
            "analytics"
        ],

        "Inventory Planner": [
            "inventory",
            "stock optimization"
        ],

        "S&OP Analyst": [
            "s&op",
            "sales and operations"
        ],

        "Material Planner": [
            "mrp",
            "material planning"
        ]
    }



    for role, keywords in roles.items():

        for word in keywords:

            if word in text:

                profile["job_titles"].append(role)

                break



    # Skills

    skills = [
        "SAP",
        "Excel",
        "Power BI",
        "Forecasting",
        "Inventory Optimization",
        "VBA"
    ]


    for skill in skills:

        if skill.lower() in text:

            profile["keywords"].append(skill)



    # Remove duplicates

    profile["job_titles"] = list(
        set(profile["job_titles"])
    )


    profile["keywords"] = list(
        set(profile["keywords"])
    )


    return profile