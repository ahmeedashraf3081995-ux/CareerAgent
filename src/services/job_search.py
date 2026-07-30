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

            seen.add(key)

            unique.append(job)

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
    # Read Parameters
    # ========================================================

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

    # ========================================================
    # Job Posting Date Filter
    #
    # 1  = last 1 day
    # 3  = last 3 days
    # 7  = last 7 days
    # 14 = last 14 days
    # 30 = last 30 days
    # 0  = any time
    #
    # Default = 7 days
    # ========================================================

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

    print(
        "=================================================="
    )

    print(
        "JOB SEARCH DATE FILTER"
    )

    if posted_days > 0:

        print(
            f"Requested: Last {posted_days} days"
        )

    else:

        print(
            "Requested: Any time"
        )

    print(
        "=================================================="
    )

    # ========================================================
    # Default Search Titles
    # ========================================================

    if not job_titles:

        job_titles = [

            "Demand Planner",

            "Supply Planner"

        ]

    # ========================================================
    # Expand Titles
    # ========================================================

    job_titles = expand_titles(
        job_titles
    )

    print(
        "Expanded titles:"
    )

    print(
        job_titles
    )

    # ========================================================
    # Default Cities
    # ========================================================

    if not cities:

        cities = [
            "Dubai"
        ]

    # ========================================================
    # LinkedIn Search
    # ========================================================

    for title in job_titles:

        for city in cities:

            print(
                ""
            )

            print(
                "=================================================="
            )

            print(
                f"Searching: {title} - {city}"
            )

            print(
                "=================================================="
            )

            try:

                jobs = scrape_linkedin(

                    keyword=title,

                    location=city,

                    pages=5,

                    posted_days=posted_days

                )

            except Exception as e:

                print(
                    f"LinkedIn search failed "
                    f"for {title} - {city}:"
                )

                print(
                    repr(e)
                )

                continue

            if not jobs:

                print(
                    "No jobs returned."
                )

                continue

            # =================================================
            # Company Filter
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
                            in
                            company_name
                        ):

                            allowed = True

                            break

                    if not allowed:

                        continue

                results.append(
                    job
                )

    # ========================================================
    # Raw Jobs
    # ========================================================

    print(
        ""
    )

    print(
        "Raw jobs before duplicate removal:",
        len(results)
    )

    # ========================================================
    # Remove Duplicates
    # ========================================================

    results = clean_jobs(
        results
    )

    print(
        "Unique jobs:",
        len(results)
    )

    # ========================================================
    # Smart Pre Filter
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
                repr(e)
            )

        print(
            "After relevance filter:",
            len(results)
        )

    # ========================================================
    # Load Job Descriptions
    # ========================================================

    if results:

        try:

            results = load_descriptions(
                results
            )

        except Exception as e:

            print(
                "Description loading failed:",
                repr(e)
            )

    # ========================================================
    # Description Statistics
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
    # Save Filters
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
            repr(e)
        )

    # ========================================================
    # Final Statistics
    # ========================================================

    print(
        ""
    )

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
        f"Posted-days filter: "
        f"{posted_days if posted_days > 0 else 'Any time'}"
    )

    print(
        "=================================================="
    )

    return results