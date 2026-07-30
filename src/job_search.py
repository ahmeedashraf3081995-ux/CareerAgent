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
# Normalize Text
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    return (
        str(text)
        .lower()
        .strip()
    )


# ============================================================
# Job Title Matching
# ============================================================

def title_matches(
    job_title,
    requested_titles
):

    if not job_title:

        return False

    normalized_job_title = normalize_text(
        job_title
    )

    for title in requested_titles:

        normalized_title = normalize_text(
            title
        )

        if not normalized_title:

            continue

        # ----------------------------------------------------
        # Direct title match
        # ----------------------------------------------------

        if normalized_title in normalized_job_title:

            return True

        # ----------------------------------------------------
        # Handle common punctuation differences
        # ----------------------------------------------------

        compact_job_title = (
            normalized_job_title
            .replace("-", " ")
            .replace("/", " ")
            .replace("&", "and")
        )

        compact_title = (
            normalized_title
            .replace("-", " ")
            .replace("/", " ")
            .replace("&", "and")
        )

        if compact_title in compact_job_title:

            return True

    return False


# ============================================================
# Job Title Filter
# ============================================================

def filter_by_job_titles(
    jobs,
    requested_titles
):

    if not requested_titles:

        return jobs

    filtered = []

    for job in jobs:

        title = job.get(
            "job_title",
            ""
        )

        if title_matches(
            title,
            requested_titles
        ):

            filtered.append(
                job
            )

    return filtered


# ============================================================
# Company Filter
# ============================================================

def filter_by_companies(
    jobs,
    companies
):

    if not companies:

        return jobs

    filtered = []

    for job in jobs:

        company_name = normalize_text(
            job.get(
                "company",
                ""
            )
        )

        allowed = False

        for company in companies:

            company_filter = normalize_text(
                company
            )

            if (
                company_filter
                and
                company_filter in company_name
            ):

                allowed = True

                break

        if allowed:

            filtered.append(
                job
            )

    return filtered


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
    # LOG SEARCH ORDER
    # ========================================================

    print("")
    print("==================================================")
    print("JOB SEARCH PIPELINE")
    print("==================================================")

    print(
        "1. Country:",
        countries if countries else "Default"
    )

    print(
        "2. City:",
        cities if cities else "Default"
    )

    print(
        "3. Posted days:",
        (
            f"Last {posted_days} days"
            if posted_days > 0
            else "Any time"
        )
    )

    print(
        "4. Job titles:",
        job_titles if job_titles else "Default"
    )

    print(
        "5. Companies:",
        companies if companies else "All"
    )

    print("==================================================")

    # ========================================================
    # STEP 2
    # Default Job Titles
    # ========================================================

    if not job_titles:

        job_titles = [

            "Demand Planner",

            "Supply Planner"

        ]

    # ========================================================
    # STEP 3
    # Expand Titles
    # ========================================================

    job_titles = expand_titles(
        job_titles
    )

    print("")
    print(
        "Expanded job titles:"
    )

    print(
        job_titles
    )

    # ========================================================
    # STEP 4
    # Default Country
    # ========================================================

    if not countries:

        countries = [

            "United Arab Emirates"

        ]

    # ========================================================
    # STEP 5
    # Default City
    # ========================================================

    if not cities:

        cities = [

            "Dubai"

        ]

    # ========================================================
    # IMPORTANT SEARCH STRATEGY
    #
    # We DO NOT search LinkedIn separately for every title.
    #
    # Instead:
    #
    # Country
    #     ↓
    # City
    #     ↓
    # Last X Days
    #     ↓
    # Collect job cards
    #     ↓
    # Filter job titles locally
    #     ↓
    # Filter companies
    #
    # This prevents opening/scraping individual job pages
    # before we know whether the job is relevant.
    # ========================================================

    for country in countries:

        for city in cities:

            if country:

                search_location = (
                    f"{city}, {country}"
                )

            else:

                search_location = city

            print("")
            print(
                "=================================================="
            )

            print(
                f"LOCATION: {search_location}"
            )

            print(
                f"DATE FILTER: "
                f"{posted_days} days"
            )

            print(
                "TITLE FILTER: Applied AFTER job cards are collected"
            )

            print(
                "=================================================="
            )

            # =================================================
            # SEARCH LOCATION + DATE FIRST
            #
            # Empty keyword means LinkedIn returns jobs for
            # the location/date rather than running a separate
            # LinkedIn search for every title.
            # =================================================

            try:

                jobs = scrape_linkedin(

                    keyword="",

                    location=search_location,

                    pages=5,

                    posted_days=posted_days

                )

            except Exception as e:

                print(
                    f"LinkedIn search failed "
                    f"for {search_location}:",
                    e
                )

                continue

            if not jobs:

                print(
                    "No jobs returned."
                )

                continue

            print(
                f"Location/date jobs returned: "
                f"{len(jobs)}"
            )

            # =================================================
            # JOB TITLE FILTER
            # =================================================

            before_title_filter = len(
                jobs
            )

            jobs = filter_by_job_titles(

                jobs,

                job_titles

            )

            print(
                f"After job title filter: "
                f"{len(jobs)} "
                f"/ {before_title_filter}"
            )

            # =================================================
            # COMPANY FILTER
            # =================================================

            before_company_filter = len(
                jobs
            )

            jobs = filter_by_companies(

                jobs,

                companies

            )

            print(
                f"After company filter: "
                f"{len(jobs)} "
                f"/ {before_company_filter}"
            )

            results.extend(
                jobs
            )

    # ========================================================
    # RAW RESULTS
    # ========================================================

    print("")
    print(
        "=================================================="
    )

    print(
        "RAW FILTERED JOBS"
    )

    print(
        f"Jobs after country/city/date/title/company filters: "
        f"{len(results)}"
    )

    print(
        "=================================================="
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    results = clean_jobs(
        results
    )

    print(
        f"Unique jobs: {len(results)}"
    )

    # ========================================================
    # SMART PRE FILTER
    #
    # This still happens BEFORE descriptions are loaded.
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
    # ONLY jobs that survived all previous filters reach here.
    #
    # This is the expensive operation we want to minimize.
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
        f"Descriptions loaded: "
        f"{descriptions_loaded}"
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