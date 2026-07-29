def expand_titles(user_titles):

    expanded = []


    title_map = {

        # ==========================
        # Demand Planning
        # ==========================

        "demand": [

            "Demand Planner",
            "Senior Demand Planner",
            "Demand Planning Specialist",
            "Demand Planning Analyst",
            "Demand Planning Lead",
            "Demand Planning Manager",
            "Senior Demand Planning Manager",
            "Regional Demand Planning Manager",
            "Head of Demand Planning",
            "Director of Demand Planning"

        ],


        # ==========================
        # Supply Planning
        # ==========================

        "supply": [

            "Supply Planner",
            "Senior Supply Planner",
            "Supply Planning Specialist",
            "Supply Planning Analyst",
            "Supply Planning Lead",
            "Supply Planning Manager",
            "Senior Supply Planning Manager",
            "Regional Supply Planning Manager",
            "Head of Supply Planning"

        ],


        # ==========================
        # Inventory
        # ==========================

        "inventory": [

            "Inventory Planner",
            "Senior Inventory Planner",
            "Inventory Analyst",
            "Inventory Planning Specialist",
            "Inventory Control Manager",
            "Inventory Planning Manager",
            "Stock Planning Manager"

        ],


        # ==========================
        # S&OP
        # ==========================

        "s&op": [

            "S&OP Analyst",
            "S&OP Specialist",
            "S&OP Planner",
            "S&OP Lead",
            "S&OP Manager",
            "Sales and Operations Planning Manager",
            "Head of S&OP"

        ],


        # ==========================
        # Merchandise Planning
        # ==========================

        "merchandise": [

            "Merchandise Planner",
            "Senior Merchandise Planner",
            "Merchandise Planning Specialist",
            "Merchandise Planning Manager",
            "Retail Planner",
            "Retail Planning Manager",
            "Category Planner"

        ],


        # ==========================
        # General Planning
        # ==========================

        "planning": [

            "Planning Analyst",
            "Planning Specialist",
            "Senior Planner",
            "Planning Lead",
            "Planning Manager",
            "Senior Planning Manager",
            "Regional Planning Manager",
            "Head of Planning"

        ],


        # ==========================
        # Supply Chain
        # ==========================

        "supply chain": [

            "Supply Chain Analyst",
            "Senior Supply Chain Analyst",
            "Supply Chain Specialist",
            "Supply Chain Planner",
            "Supply Chain Manager",
            "Regional Supply Chain Manager"

        ]

    }



    for title in user_titles:


        title_lower = title.lower()


        matched = False


        for keyword, variations in title_map.items():


            if keyword in title_lower:


                expanded.extend(
                    variations
                )

                matched = True



        # Keep original title if no match

        if not matched:


            expanded.append(
                title
            )



    # Remove duplicates while preserving order

    return list(
        dict.fromkeys(
            expanded
        )
    )