from src.scrapers.linkedin_scraper import scrape_linkedin
from src.services.title_expander import expand_titles
from src.services.description_loader import load_descriptions
from src.services.job_pre_filter import pre_filter_jobs





def clean_jobs(jobs):

    unique = []

    seen = set()


    for job in jobs:


        key = (

            job.get(
                "job_title",
                ""
            )
            .lower()

            +

            job.get(
                "company",
                ""
            )
            .lower()

            +

            job.get(
                "location",
                ""
            )
            .lower()

        )


        if key not in seen:

            seen.add(
                key
            )

            unique.append(
                job
            )


    return unique





def extract_job_filters(jobs):


    filters = {


        "titles": [],

        "companies": [],

        "locations": []

    }



    for job in jobs:


        title = job.get(
            "job_title",
            ""
        )


        company = job.get(
            "company",
            ""
        )


        location = job.get(
            "location",
            ""
        )



        if title and title not in filters["titles"]:


            filters["titles"].append(
                title
            )



        if company and company not in filters["companies"]:


            filters["companies"].append(
                company
            )



        if location and location not in filters["locations"]:


            filters["locations"].append(
                location
            )



    return filters






def search_jobs(parameters):


    results = []



    job_titles = parameters.get(

        "job_titles",

        []

    )


    cities = parameters.get(

        "cities",

        []

    )


    companies = parameters.get(

        "companies",

        []

    )


    cv_text = parameters.get(

        "cv_text",

        ""

    )





    # ==========================
    # Default Search
    # ==========================

    if not job_titles:


        job_titles = [

            "Demand Planner",

            "Supply Planner"

        ]





    # ==========================
    # Expand Titles
    # ==========================

    job_titles = expand_titles(

        job_titles

    )



    print(
        "Expanded titles:"
    )


    print(
        job_titles
    )





    # ==========================
    # Default Cities
    # ==========================

    if not cities:


        cities = [

            "Dubai"

        ]





    # ==========================
    # LinkedIn Search
    # ==========================

    for title in job_titles:


        for city in cities:


            print(

                f"Searching {title} - {city}"

            )



            jobs = scrape_linkedin(

                keyword=title,

                location=city,

                pages=5

            )



            for job in jobs:



                # --------------------------
                # Company Filter
                # --------------------------

                if companies:


                    company_name = job.get(

                        "company",

                        ""

                    ).lower()



                    allowed = False



                    for company in companies:


                        if company.lower() in company_name:


                            allowed = True



                            break



                    if not allowed:


                        continue




                results.append(
                    job
                )






    print(

        "Raw jobs:",

        len(results)

    )






    # ==========================
    # Remove Duplicates
    # ==========================

    results = clean_jobs(

        results

    )



    print(

        "Unique jobs:",

        len(results)

    )







    # ==========================
    # Smart Pre Filter
    # ==========================

    if cv_text:


        results = pre_filter_jobs(

            cv_text,

            results,

            limit=100

        )



        print(

            "After relevance filter:",

            len(results)

        )







    # ==========================
    # Load Descriptions
    # ==========================

    results = load_descriptions(

        results

    )



    print(

        "Descriptions loaded:",

        len(results)

    )







    # ==========================
    # Save Filters
    # ==========================

    try:


        import streamlit as st


        st.session_state.job_filters = extract_job_filters(

            results

        )


    except Exception as e:


        print(

            "Filter save skipped:",

            e

        )






    return results