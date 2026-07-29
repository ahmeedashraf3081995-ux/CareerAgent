def expand_titles(user_titles):


    expanded = []


    title_map = {


        "demand": [

            "Demand Planner",

            "Senior Demand Planner",

            "Demand Planning Specialist",

            "Demand Planning Lead",

            "Demand Planning Manager"

        ],



        "supply": [

            "Supply Planner",

            "Senior Supply Planner",

            "Supply Planning Specialist",

            "Supply Planning Lead",

            "Supply Planning Manager"

        ],



        "inventory": [

            "Inventory Planner",

            "Senior Inventory Planner",

            "Inventory Planning Manager"

        ],



        "s&op": [

            "S&OP Analyst",

            "S&OP Specialist",

            "S&OP Manager"

        ],



        "merchandise": [

            "Merchandise Planner",

            "Senior Merchandise Planner",

            "Merchandise Planning Manager"

        ],



        "planning": [

            "Planning Analyst",

            "Senior Planner",

            "Planning Manager",

            "Regional Planning Manager"

        ]

    }




    for title in user_titles:


        title_lower = title.lower()


        matched = False



        for key, values in title_map.items():


            if key in title_lower:


                expanded.extend(values)

                matched = True



        if not matched:


            expanded.append(title)




    # Remove duplicates and limit search volume

    final_titles = list(

        dict.fromkeys(

            expanded

        )

    )



    return final_titles[:5]