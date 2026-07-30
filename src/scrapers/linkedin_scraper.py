from playwright.sync_api import sync_playwright
import urllib.parse
import time
import shutil
import os


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

    # Streamlit Cloud / Linux
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
# LinkedIn Job Search
# ============================================================

def scrape_linkedin(
    keyword="Demand Planner",
    location="Dubai",
    pages=1,
    posted_days=None
):

    print(
        f"Searching LinkedIn: {keyword} - {location}"
    )

    if posted_days:

        print(
            f"LinkedIn date filter: last {posted_days} days"
        )

    else:

        print(
            "LinkedIn date filter: Any time"
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
                # Date Posted Filter
                #
                # LinkedIn f_TPR uses seconds.
                #
                # Example:
                # 1 day  = r86400
                # 7 days = r604800
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
                    f"Opening LinkedIn page {page_number + 1}"
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
                            e
                        )

        except Exception as e:

            print(
                "LinkedIn scraper error:",
                e
            )

        finally:

            browser.close()

    print(
        "Total collected:",
        len(jobs)
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
                e
            )

            description = ""

        finally:

            browser.close()

    return description