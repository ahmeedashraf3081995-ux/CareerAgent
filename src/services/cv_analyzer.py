import re



def clean_title(title):

    title = title.strip()

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title



def analyze_cv(text):


    text_lower = text.lower()



    job_titles = []



    # =====================================
    # Extract real experience titles
    # =====================================

    title_patterns = [


        r"(assistant manager[^|\n]*)",
        r"(senior planner[^|\n]*)",
        r"(regional demand planning lead[^|\n]*)",
        r"(demand planning lead[^|\n]*)",
        r"(supply chain analyst[^|\n]*)",
        r"(supply planner[^|\n]*)",
        r"(demand planner[^|\n]*)",
        r"(planning manager[^|\n]*)",
        r"(material requirement planning[^|\n]*)",
        r"(material planning engineer[^|\n]*)"


    ]



    for pattern in title_patterns:


        matches = re.findall(
            pattern,
            text_lower
        )


        for match in matches:


            title = clean_title(
                match
            )


            if len(title) > 5:

                job_titles.append(
                    title.title()
                )



    # =====================================
    # Add recommended roles
    # only from strong evidence
    # =====================================


    if (
        "forecast" in text_lower
        and "inventory" in text_lower
    ):

        job_titles.append(
            "Demand Planner"
        )


    if (
        "supply planning" in text_lower
        or "supply planner" in text_lower
    ):

        job_titles.append(
            "Supply Planner"
        )


    if (
        "inventory optimization" in text_lower
        or "stock level" in text_lower
    ):

        job_titles.append(
            "Inventory Planner"
        )


    if (
        "otb" in text_lower
        or "merchandising" in text_lower
    ):

        job_titles.append(
            "Merchandise Planner"
        )



    # =====================================
    # Remove bad generic titles
    # =====================================

    blacklist = [

        "Manager",
        "Senior Specialist",
        "Director",
        "Analyst"

    ]


    job_titles = [

        x for x in job_titles
        if x not in blacklist

    ]



    # Limit results

    job_titles = list(
        dict.fromkeys(
            job_titles
        )
    )[:8]



    # =====================================
    # Countries
    # =====================================

    countries=[]


    country_map = {

        "uae":"UAE",
        "dubai":"UAE",
        "abu dhabi":"UAE",

        "saudi":"Saudi Arabia",
        "riyadh":"Saudi Arabia",

        "qatar":"Qatar",
        "doha":"Qatar",

        "egypt":"Egypt",
        "cairo":"Egypt",

        "uk":"United Kingdom",
        "london":"United Kingdom"

    }



    for key,value in country_map.items():

        if key in text_lower:

            if value not in countries:

                countries.append(value)



    # =====================================
    # Cities
    # =====================================

    cities=[]


    city_map = {

        "dubai":"Dubai",
        "abu dhabi":"Abu Dhabi",
        "riyadh":"Riyadh",
        "jeddah":"Jeddah",
        "doha":"Doha",
        "cairo":"Cairo",
        "london":"London"

    }



    for key,value in city_map.items():

        if key in text_lower:

            if value not in cities:

                cities.append(value)



    return {


        "job_titles": job_titles,

        "countries": countries,

        "cities": cities

    }