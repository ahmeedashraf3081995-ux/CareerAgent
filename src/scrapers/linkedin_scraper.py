from playwright.sync_api import sync_playwright
import urllib.parse
import time
import shutil
import os
import re
from datetime import datetime, timedelta


# ============================================================
# Browser Configuration
# ============================================================

def launch_browser(playwright):

    """
    Launch Chromium.

    Streamlit Cloud / Linux:
        Use system Chromium installed through packages.txt.

    Windows:
        Use Playwright's bundled Chromium.
    """

    system_chromium = None

    # ========================================================
    # Linux / Streamlit Cloud
    # ========================================================

    if os.name != "nt":

        possible_browsers = [

            "chromium",

            "chromium-browser",

            "google-chrome"

        ]

        for browser_name in possible_browsers:

            browser_path = shutil.which(
                browser_name
            )

            if browser_path:

                system_chromium = browser_path

                break

    # ========================================================
    # System Chromium
    # ========================================================

    if system_chromium:

        print(
            f"Using system Chromium: {system_chromium}"
        )

        return playwright.chromium.launch(

            headless=True,

            executable_path=system_chromium,

            args=[

                "--no-sandbox",

                "--disable-dev-shm-usage",

                "--disable-gpu",

                "--disable-setuid-sandbox",

                "--disable-software-rasterizer"

            ]

        )

    # ========================================================
    # Playwright Chromium
    # ========================================================

    print(
        "Using Playwright Chromium."
    )

    return playwright.chromium.launch(

        headless=True,

        args=[

            "--no-sandbox",

            "--disable-dev-shm-usage",

            "--disable-gpu"

        ]

    )


# ============================================================
# Parse LinkedIn Posted Date
# ============================================================

def parse_posted_date(posted_text):

    """
    Convert LinkedIn date text into a datetime.

    Examples:

        "1 day ago"
        "2 days ago"
        "1 week ago"
        "2 weeks ago"
        "3 hours ago"
        "30 minutes ago"
        "just now"
        "today"
        "yesterday"
    """

    if not posted_text:

        return None

    text = (
        str(posted_text)
        .lower()
        .strip()
    )

    # Remove extra whitespace

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    now = datetime.now()

    # ========================================================
    # Just now
    # ========================================================

    if (
        "just now" in text
        or
        "moments ago" in text
    ):

        return now

    # ========================================================
    # Today
    # ========================================================

    if text == "today":

        return now

    # ========================================================
    # Yesterday
    # ========================================================

    if text == "yesterday":

        return now - timedelta(
            days=1
        )

    # ========================================================
    # Minutes
    # ========================================================

    match = re.search(
        r"(\d+)\s*(minute|minutes|min|mins)\s*ago",
        text
    )

    if match:

        minutes = int(
            match.group(1)
        )

        return now - timedelta(
            minutes=minutes
        )

    # ========================================================
    # Hours
    # ========================================================

    match = re.search(
        r"(\d+)\s*(hour|hours|hr|hrs)\s*ago",
        text
    )

    if match:

        hours = int(
            match.group(1)
        )

        return now - timedelta(
            hours=hours
        )

    # ========================================================
    # Days
    # ========================================================

    match = re.search(
        r"(\d+)\s*(day|days)\s*ago",
        text
    )

    if match:

        days = int(
            match.group(1)
        )

        return now - timedelta(
            days=days
        )

    # ========================================================
    # Weeks
    # ========================================================

    match = re.search(
        r"(\d+)\s*(week|weeks)\s*ago",
        text
    )

    if match:

        weeks = int(
            match.group(1)
        )

        return now - timedelta(
            weeks=weeks
        )

    # ========================================================
    # Months
    # ========================================================

    match = re.search(
        r"(\d+)\s*(month|months)\s*ago",
        text
    )

    if match:

        months = int(
            match.group(1)
        )

        return now - timedelta(
            days=months * 30
        )

    # ========================================================
    # Years
    # ========================================================

    match = re.search(
        r"(\d+)\s*(year|years)\s*ago",
        text
    )

    if match:

        years = int(
            match.group(1)
        )

        return now - timedelta(
            days=years * 365
        )

    # ========================================================
    # Unknown format
    # ========================================================

    return None


# ============================================================
# Check Date Filter
# ============================================================

def is_within_posted_days(
    posted_text,
    posted_days
):

    """
    Returns:

        True  = job should be kept
        False = job should be removed

    Important:
        If LinkedIn gives an unknown date format,
        we KEEP the job rather than accidentally deleting it.
    """

    # ========================================================
    # No filter
    # ========================================================

    if not posted_days:

        return True

    try:

        posted_days = int(
            posted_days
        )

    except Exception:

        return True

    if posted_days <= 0:

        return True

    # ========================================================
    # Parse date
    # ========================================================

    posted_datetime = parse_posted_date(
        posted_text
    )

    # ========================================================
    # Unknown date
    # ========================================================

    if posted_datetime is None:

        print(
            f"WARNING: Could not parse LinkedIn date: "
            f"'{posted_text}'"
        )

        # Keep it because we don't want to
        # accidentally remove valid jobs.

        return True

    # ========================================================
    # Compare
    # ========================================================

    cutoff = (
        datetime.now()
        -
        timedelta(
            days=posted_days
        )
    )

    return posted_datetime >= cutoff


# ============================================================
# LinkedIn Job Search
# ============================================================

def scrape_linkedin(
    keyword="Demand Planner",
    location="Dubai",
    pages=1,
    posted_days=None
):

    print(
        ""
    )

    print(
        "=================================================="
    )

    print(
        f"Searching LinkedIn: "
        f"{keyword} - {location}"
    )

    if posted_days:

        print(
            f"LinkedIn date filter: "
            f"last {posted_days} days"
        )

    else:

        print(
            "LinkedIn date filter: Any time"
        )

    print(
        "=================================================="
    )

    jobs = []

    seen = set()

    filtered_out = 0

    unknown_dates = 0

    with sync_playwright() as p:

        browser = launch_browser(p)

        page = browser.new_page(

            viewport={
                "width": 1920,
                "height": 1080
            }

        )

        try:

            for page_number in range(pages):

                start = page_number * 25

                # ====================================================
                # LinkedIn URL
                # ====================================================

                url = (
                    "https://www.linkedin.com/jobs/search/?keywords="
                    +
                    urllib.parse.quote(keyword)
                    +
                    "&location="
                    +
                    urllib.parse.quote(location)
                    +
                    "&start="
                    +
                    str(start)
                )

                # ====================================================
                # LinkedIn Server-Side Date Filter
                # ====================================================

                if posted_days:

                    seconds = (

                        int(posted_days)

                        *
                        24

                        *
                        60

                        *
                        60

                    )

                    url += (
                        "&f_TPR=r"
                        +
                        str(seconds)
                    )

                print(
                    ""
                )

                print(
                    f"Opening LinkedIn page "
                    f"{page_number + 1}"
                )

                print(
                    "URL:",
                    url
                )

                try:

                    page.goto(

                        url,

                        timeout=20000,

                        wait_until="domcontentloaded"

                    )

                except Exception as e:

                    print(
                        "Page loading timeout:",
                        repr(e)
                    )

                    continue

                time.sleep(1)

                cards = page.locator(
                    ".base-search-card"
                )

                count = cards.count()

                print(
                    "Cards found:",
                    count
                )

                for i in range(count):

                    try:

                        card = cards.nth(i)

                        # ====================================================
                        # Title
                        # ====================================================

                        title = card.locator(
                            ".base-search-card__title"
                        ).inner_text(
                            timeout=5000
                        ).strip()

                        # ====================================================
                        # Company
                        # ====================================================

                        company = card.locator(
                            ".base-search-card__subtitle"
                        ).inner_text(
                            timeout=5000
                        ).strip()

                        # ====================================================
                        # Location
                        # ====================================================

                        location_text = card.locator(
                            ".job-search-card__location"
                        ).inner_text(
                            timeout=5000
                        ).strip()

                        # ====================================================
                        # URL
                        # ====================================================

                        link = card.locator(
                            "a"
                        ).first.get_attribute(
                            "href"
                        )

                        # ====================================================
                        # Posted Date
                        # ====================================================

                        posted_date = ""

                        date_selectors = [

                            "time",

                            ".job-search-card__listdate",

                            ".job-search-card__listdate--new"

                        ]

                        for selector in date_selectors:

                            try:

                                date_element = card.locator(
                                    selector
                                ).first

                                if date_element.count() > 0:

                                    posted_date = (

                                        date_element

                                        .inner_text(
                                            timeout=2000
                                        )

                                        .strip()

                                    )

                                    if posted_date:

                                        break

                            except Exception:

                                continue

                        # ====================================================
                        # HARD PYTHON DATE FILTER
                        # ====================================================

                        if posted_days:

                            parsed_date = parse_posted_date(
                                posted_date
                            )

                            if parsed_date is None:

                                unknown_dates += 1

                            else:

                                if not is_within_posted_days(

                                    posted_date,

                                    posted_days

                                ):

                                    filtered_out += 1

                                    print(

                                        f"FILTERED OUT: "
                                        f"{title} | "
                                        f"{posted_date}"

                                    )

                                    continue

                        # ====================================================
                        # Duplicate Check
                        # ====================================================

                        key = (

                            title.lower()

                            +

                            company.lower()

                            +

                            location_text.lower()

                        )

                        if key in seen:

                            continue

                        seen.add(
                            key
                        )

                        # ====================================================
                        # Save Job
                        # ====================================================

                        jobs.append({

                            "job_title":
                                title,

                            "company":
                                company,

                            "location":
                                location_text,

                            "url":
                                link,

                            "source":
                                "LinkedIn",

                            "posted_date":
                                posted_date,

                            "description":
                                ""

                        })

                    except Exception as e:

                        print(
                            "Card skipped:",
                            repr(e)
                        )

        except Exception as e:

            print(
                "LinkedIn scraper error:",
                repr(e)
            )

        finally:

            browser.close()

    # ============================================================
    # Statistics
    # ============================================================

    print(
        ""
    )

    print(
        "=================================================="
    )

    print(
        "LINKEDIN SCRAPER COMPLETED"
    )

    print(
        f"Jobs kept: {len(jobs)}"
    )

    print(
        f"Jobs removed by date filter: "
        f"{filtered_out}"
    )

    print(
        f"Unknown date formats: "
        f"{unknown_dates}"
    )

    print(
        "=================================================="
    )

    return jobs


# ============================================================
# Extract Job Description
# ============================================================

def extract_job_details(url):

    if not url:

        return ""

    description = ""

    with sync_playwright() as p:

        browser = launch_browser(p)

        page = browser.new_page(

            viewport={
                "width": 1920,
                "height": 1080
            }

        )

        try:

            print(
                f"Opening job details: {url}"
            )

            page.goto(

                url,

                timeout=15000,

                wait_until="domcontentloaded"

            )

            time.sleep(0.8)

            selectors = [

                ".show-more-less-html__markup",

                ".description__text",

                ".decorated-job-posting__details",

                ".jobs-description__content"

            ]

            for selector in selectors:

                try:

                    element = page.locator(
                        selector
                    ).first

                    if element.count() > 0:

                        text = element.inner_text(
                            timeout=3000
                        ).strip()

                        if text:

                            description = text

                            break

                except Exception:

                    continue

            if not description:

                try:

                    description = page.locator(
                        "body"
                    ).inner_text(
                        timeout=3000
                    ).strip()

                except Exception:

                    description = ""

        except Exception as e:

            print(
                "Job detail error:",
                repr(e)
            )

            description = ""

        finally:

            browser.close()

    return description