import json
import os


JOBS_FILE = "data/jobs/jobs_database.json"

LOCATIONS_FILE = "data/config/locations.json"
ROLES_FILE = "data/config/job_roles.json"



def load_jobs():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_json(data, filename):

    os.makedirs(
        "data/config",
        exist_ok=True
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )



def extract_locations(jobs):

    locations = set()


    for job in jobs:

        location = job.get(
            "location",
            ""
        ).strip()


        if location:

            locations.add(location)



    return sorted(
        list(locations)
    )



def extract_roles(jobs):

    roles = set()


    # Planning job families
    keywords = [

        "Demand Planner",
        "Demand Planning",

        "Supply Planner",
        "Supply Planning",

        "Material Planner",
        "Material Planning",

        "Planning Manager",

        "S&OP",
        "S&OP Planner",

        "Inventory Planner",
        "Inventory Planning",

        "Replenishment Planner",

        "Production Planner",
        "Production Planning",

        "Supply Chain Planner",

        "Forecasting",

        "MRP",

        "Sales and Operations Planning"

    ]



    for job in jobs:


        title = job.get(
            "job_title",
            ""
        )


        description = job.get(
            "description",
            ""
        )


        text = (
            title
            + " "
            + description
        ).lower()



        for keyword in keywords:


            if keyword.lower() in text:

                roles.add(keyword)



    return sorted(
        list(roles)
    )



if __name__ == "__main__":


    print(
        "Filter Configuration Engine\n"
    )


    jobs = load_jobs()



    locations = extract_locations(
        jobs
    )


    roles = extract_roles(
        jobs
    )



    save_json(
        locations,
        LOCATIONS_FILE
    )


    save_json(
        roles,
        ROLES_FILE
    )



    print(
        "Configuration created"
    )


    print(
        "Locations found:",
        len(locations)
    )


    print(
        "Roles found:",
        len(roles)
    )



    print(
        "\nLocations:"
    )


    for location in locations:

        print(
            "-",
            location
        )



    print(
        "\nRoles:"
    )


    for role in roles:

        print(
            "-",
            role
        )