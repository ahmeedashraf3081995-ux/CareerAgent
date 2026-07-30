from playwright.sync_api import sync_playwright
import urllib.parse
import time
import shutil
import os
import re


# ============================================================
# Browser Configuration
# ============================================================

def launch_browser(playwright):

    """
    Launch Chromium.

    Linux / Streamlit Cloud:
        Use installed Chromium when available.

    Windows:
        Use Playwright's bundled Chromium.
    """

    system_chromium = None

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
# Helpers
# ============================================================

def normalize_posted_date(text):

    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip().lower()


def is_recent_job(
    posted_date,
    posted_days
):

    """
    Secondary safety filter.

    LinkedIn f_TPR is the primary date filter.

    This prevents old jobs from slipping through if
    LinkedIn returns a stale card.
    """

    if not posted_days:
        return True

    if not posted_date:
        return True

    text = normalize_posted_date(
        posted_date
    )

    numbers = re.findall(
        r"\d+",
        text
    )

    number = (
        int(numbers[0])
        if numbers
        else 1
    )

    if "minute" in text:
        age_days = 0

    elif "hour" in text:
        age_days = 0

    elif "day" in text:
        age_days = number

    elif "week" in text:
        age_days = number * 7

    elif "month" in text:
        age_days = number * 30

    elif "year" in text:
        age_days = number * 365

    elif "just now" in text:
        age_days = 0

    elif "today" in text:
        age_days = 0

    else:
        return True

    return age_days <= int(posted_days)


def normalize_title(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s&/-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def title_matches(
    title,
    keywords
):

    """
    Check whether a LinkedIn job title matches
    one of the requested titles.

    Used only when a broad location/date search
    is requested.
    """

    if not keywords:
        return True

    normalized_title = normalize_title(
        title
    )

    for keyword in keywords:

        normalized_keyword = normalize_title(
            keyword
        )

        if not normalized_keyword:
            continue

        if normalized_keyword in normalized_title:
            return True

    return False


def extract_card_data(
    card
):

    """
    Extract only lightweight information from a
    LinkedIn search card.

    IMPORTANT:
    This does NOT open the individual job page.
    """

    title = card.locator(
        ".base-search-card__title"
    ).inner_text(
        timeout=5000
    ).strip()

    company = card.locator(
        ".base-search-card__subtitle"
    ).inner_text(
        timeout=5000
    ).strip()

    location_text = card.locator(
        ".job-search-card__location"
    ).inner_text(
        timeout=5000
    ).strip()

    link = card.locator(
        "a"
    ).first.get_attribute(
        "href"
    )

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

    return {

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

    }


# ============================================================
# LinkedIn Search
# ============================================================

def scrape_linkedin(
    keyword="Demand Planner",
    location="Dubai",
    pages=1,
    posted_days=None,
    title_filter=None
):

    """
    Search LinkedIn jobs.

    Pipeline:

        LOCATION
            ↓
        DATE FILTER
            ↓
        TITLE SEARCH
            ↓
        SECONDARY DATE VALIDATION
            ↓
        RETURN LIGHTWEIGHT JOB CARDS

    Individual job descriptions are NOT opened here.
    """

    print("")
    print(
        "=================================================="
    )

    print(
        "LINKEDIN SEARCH"
    )

    print(
        f"Location: {location}"
    )

    print(
        f"Keyword: {keyword}"
    )

    if posted_days:

        print(
            f"Date: LAST {posted_days} DAYS"
        )

    else:

        print(
            "Date: ANY TIME"
        )

    print(
        "=================================================="
    )

    jobs = []

    seen = set()

    with sync_playwright() as p:

        browser = launch_browser(p)

        page = browser.new_page(

            viewport={
                "width": 1920,
                "height": 1080
            }

        )

        try:

            for page_number in range(
                pages
            ):

                start = (
                    page_number
                    * 25
                )

                # ====================================================
                # LinkedIn URL
                # ====================================================

                url = (
                    "https://www.linkedin.com/jobs/search/?"
                    "keywords="
                    +
                    urllib.parse.quote(
                        keyword
                    )
                    +
                    "&location="
                    +
                    urllib.parse.quote(
                        location
                    )
                    +
                    "&start="
                    +
                    str(start)
                )

                # ====================================================
                # DATE FILTER
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

                print("")
                print(
                    f"Opening LinkedIn page "
                    f"{page_number + 1}/{pages}"
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
                        e
                    )

                    continue

                # Short wait only.
                time.sleep(0.7)

                cards = page.locator(
                    ".base-search-card"
                )

                count = cards.count()

                print(
                    "Cards found:",
                    count
                )

                if count == 0:

                    print(
                        "No cards found. "
                        "Stopping pagination."
                    )

                    break

                page_added = 0

                for i in range(
                    count
                ):

                    try:

                        card = cards.nth(i)

                        job = extract_card_data(
                            card
                        )

                        title = job.get(
                            "job_title",
                            ""
                        )

                        company = job.get(
                            "company",
                            ""
                        )

                        location_text = job.get(
                            "location",
                            ""
                        )

                        posted_date = job.get(
                            "posted_date",
                            ""
                        )

                        # =================================================
                        # TITLE FILTER
                        # =================================================

                        if title_filter:

                            if not title_matches(
                                title,
                                title_filter
                            ):

                                continue

                        # =================================================
                        # SECONDARY DATE FILTER
                        # =================================================

                        if posted_days:

                            if not is_recent_job(
                                posted_date,
                                posted_days
                            ):

                                print(
                                    f"Skipping old job: "
                                    f"{title} | "
                                    f"{posted_date}"
                                )

                                continue

                        # =================================================
                        # DUPLICATE
                        # =================================================

                        key = (

                            title.lower().strip()

                            + "|"

                            + company.lower().strip()

                            + "|"

                            + location_text.lower().strip()

                        )

                        if key in seen:
                            continue

                        seen.add(
                            key
                        )

                        jobs.append(
                            job
                        )

                        page_added += 1

                    except Exception as e:

                        print(
                            "Card skipped:",
                            e
                        )

                print(
                    f"Jobs accepted from page: "
                    f"{page_added}"
                )

        except Exception as e:

            print(
                "LinkedIn scraper error:",
                e
            )

        finally:

            browser.close()

    print("")
    print(
        f"Total jobs collected: {len(jobs)}"
    )

    return jobs


# ============================================================
# Extract Job Description
# ============================================================

def extract_job_details(
    url
):

    """
    Open an individual LinkedIn job page.

    This is intentionally separated from search scraping.

    It should only be called AFTER all lightweight
    filters have been completed.
    """

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
                e
            )

            description = ""

        finally:

            browser.close()

    return description