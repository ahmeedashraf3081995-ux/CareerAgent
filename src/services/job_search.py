from src.scrapers.linkedin_scraper import scrape_linkedin
from src.services.title_expander import expand_titles
from src.services.description_loader import load_descriptions
from src.services.job_pre_filter import pre_filter_jobs


# ============================================================
# Remove Duplicate Jobs
# ============================================================

def clean_jobs(jobs):

    unique = []

    seen = set()

    for job in jobs:

        key = (

            job.get(
                "job_title",
                ""
            ).lower().strip()

            + "|"

            + job.get(
                "company",
                ""
            ).lower().strip()

            + "|"

            + job.get(
                "location",
                ""
            ).lower().strip()

        )

        if key not in seen:

            seen.add(
                key
            )

            unique.append(
                job
            )

    return unique


# ============================================================
# Extract Filters
# ============================================================

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

        if (
            title
            and
            title not in filters["titles"]
        ):

            filters["titles"].append(
                title
            )

        if (
            company
            and
            company not in filters["companies"]
        ):

            filters["companies"].append(
                company
            )

        if (
            location
            and
            location not in filters["locations"]
        ):

            filters["locations"].append(
                location
            )

    return filters


# ============================================================
# Search Jobs
# ============================================================

def search_jobs(parameters):

    results = []

    # ========================================================
    # STEP 1
    # Read Parameters
    # ========================================================

    job_titles = parameters.get(
        "job_titles",
        []
    )

    countries = parameters.get(
        "countries",
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

    posted_days = parameters.get(
        "posted_days",
        7
    )

    try:

        posted_days = int(
            posted_days
        )

    except Exception:

        posted_days = 7

    if posted_days < 0:

        posted_days = 0

    # ========================================================
    # DEFAULT TITLES
    # ========================================================

    if not job_titles:

        job_titles = [

            "Demand Planner",

            "Supply Planner"

        ]

    # ========================================================
    # EXPAND TITLES
    # ========================================================

    job_titles = expand_titles(
        job_titles
    )

    # ========================================================
    # DEFAULT COUNTRY
    # ========================================================

    if not countries:

        countries = [

            "United Arab Emirates"

        ]

    # ========================================================
    # DEFAULT CITY
    # ========================================================

    if not cities:

        cities = [

            "Dubai"

        ]

    # ========================================================
    # LOG PIPELINE
    # ========================================================

    print("")
    print(
        "=================================================="
    )

    print(
        "JOB SEARCH PIPELINE"
    )

    print(
        "=================================================="
    )

    print(
        "1. Country:",
        countries
    )

    print(
        "2. City:",
        cities
    )

    print(
        "3. Posted:",
        (
            f"Last {posted_days} days"
            if posted_days > 0
            else "Any time"
        )
    )

    print(
        "4. Job titles:",
        job_titles
    )

    print(
        "5. Companies:",
        companies if companies else "All"
    )

    print(
        "=================================================="
    )

    # ========================================================
    # COUNTRY
    #   ↓
    # CITY
    #   ↓
    # DATE
    #   ↓
    # TITLE
    #
    # We keep the LinkedIn search lightweight.
    #
    # No individual job page is opened here.
    # ========================================================

    for country in countries:

        print("")
        print(
            "##################################################"
        )

        print(
            f"COUNTRY: {country}"
        )

        print(
            "##################################################"
        )

        for city in cities:

            if country:

                search_location = (
                    f"{city}, {country}"
                )

            else:

                search_location = city

            print("")
            print(
                "--------------------------------------------------"
            )

            print(
                f"CITY: {search_location}"
            )

            print(
                f"DATE FILTER: "
                f"{posted_days} days"
            )

            print(
                "--------------------------------------------------"
            )

            # =================================================
            # SEARCH EACH TITLE
            #
            # LinkedIn applies location + date server-side
            # BEFORE returning the job cards.
            #
            # The browser stays lightweight and NO detail
            # pages are opened at this stage.
            # =================================================

            for title in job_titles:

                print("")
                print(
                    f"TITLE SEARCH: {title}"
                )

                try:

                    jobs = scrape_linkedin(

                        keyword=title,

                        location=search_location,

                        pages=5,

                        posted_days=posted_days

                    )

                except Exception as e:

                    print(
                        f"LinkedIn search failed "
                        f"for {title} - "
                        f"{search_location}:",
                        e
                    )

                    continue

                if not jobs:

                    print(
                        "No jobs returned."
                    )

                    continue

                print(
                    f"Lightweight jobs returned: "
                    f"{len(jobs)}"
                )

                # =================================================
                # COMPANY FILTER
                #
                # Still no descriptions loaded.
                # =================================================

                for job in jobs:

                    if companies:

                        company_name = job.get(
                            "company",
                            ""
                        ).lower()

                        allowed = False

                        for company in companies:

                            if (
                                company.lower()
                                in company_name
                            ):

                                allowed = True

                                break

                        if not allowed:

                            continue

                    results.append(
                        job
                    )

    # ========================================================
    # RAW RESULTS
    # ========================================================

    print("")
    print(
        "Raw jobs after "
        "country/city/date/title/company filters:",
        len(results)
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    results = clean_jobs(
        results
    )

    print(
        "Unique jobs:",
        len(results)
    )

    # ========================================================
    # SMART PRE-FILTER
    #
    # Still happens BEFORE opening individual job pages.
    # ========================================================

    if cv_text and results:

        try:

            results = pre_filter_jobs(

                cv_text,

                results,

                limit=100

            )

        except Exception as e:

            print(
                "Pre-filter failed:",
                e
            )

        print(
            "After relevance filter:",
            len(results)
        )

    # ========================================================
    # LOAD DESCRIPTIONS
    #
    # THIS IS THE EXPENSIVE PART.
    #
    # It happens only after:
    #
    # Country
    # City
    # Date
    # Title
    # Company
    # Duplicate removal
    # Relevance filtering
    #
    # ========================================================

    if results:

        try:

            results = load_descriptions(
                results
            )

        except Exception as e:

            print(
                "Description loading failed:",
                e
            )

    # ========================================================
    # DESCRIPTION STATISTICS
    # ========================================================

    descriptions_loaded = len(

        [

            job

            for job in results

            if job.get(
                "description",
                ""
            )

        ]

    )

    print(
        "Descriptions loaded:",
        descriptions_loaded
    )

    # ========================================================
    # SAVE FILTERS
    # ========================================================

    try:

        import streamlit as st

        st.session_state.job_filters = (

            extract_job_filters(
                results
            )

        )

    except Exception as e:

        print(
            "Filter save skipped:",
            e
        )

    # ========================================================
    # FINAL
    # ========================================================

    print("")
    print(
        "=================================================="
    )

    print(
        "JOB SEARCH COMPLETED"
    )

    print(
        f"Final jobs: {len(results)}"
    )

    print(
        "=================================================="
    )

    return results