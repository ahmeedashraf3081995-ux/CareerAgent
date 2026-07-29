from playwright.sync_api import sync_playwright
import urllib.parse
import time



def scrape_linkedin(

    keyword="Demand Planner",

    location="Dubai",

    pages=1

):


    print(
        f"Searching LinkedIn: {keyword} - {location}"
    )


    jobs = []

    seen = set()



    with sync_playwright() as p:


        browser = p.chromium.launch(

            headless=True,

            executable_path="/usr/bin/chromium",

            args=[

                "--no-sandbox",

                "--disable-dev-shm-usage",

                "--disable-gpu"

            ]

        )



        page = browser.new_page(

            viewport={

                "width": 1920,

                "height": 1080

            }

        )


        try:


            for page_number in range(pages):


                start = page_number * 25



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



                print(

                    f"Opening LinkedIn page {page_number + 1}"

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



                # Allow cards to appear

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



                        title = card.locator(

                            ".base-search-card__title"

                        ).inner_text()



                        company = card.locator(

                            ".base-search-card__subtitle"

                        ).inner_text()



                        location_text = card.locator(

                            ".job-search-card__location"

                        ).inner_text()



                        link = card.locator(

                            "a"

                        ).first.get_attribute(

                            "href"

                        )



                        key = (

                            title.lower()

                            +

                            company.lower()

                            +

                            location_text.lower()

                        )



                        if key in seen:

                            continue



                        seen.add(key)



                        jobs.append(

                            {

                                "job_title": title.strip(),

                                "company": company.strip(),

                                "location": location_text.strip(),

                                "url": link,

                                "source": "LinkedIn",

                                "description": ""

                            }

                        )



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