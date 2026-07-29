from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.parse
import time





def create_driver():

    options = Options()

    options.add_argument(
        "--headless=new"
    )

    options.add_argument(
        "--disable-gpu"
    )

    options.add_argument(
        "--no-sandbox"
    )

    options.add_argument(
        "--disable-dev-shm-usage"
    )

    options.add_argument(
        "--window-size=1920,1080"
    )


    driver = webdriver.Chrome(
        options=options
    )


    driver.set_page_load_timeout(
        40
    )


    return driver





# ==================================================
# Extract Job Description
# ==================================================

def extract_job_details(driver, url):

    description = ""


    try:

        driver.get(
            url
        )


        time.sleep(2)


        elements = driver.find_elements(

            By.CLASS_NAME,

            "description__text"

        )


        if elements:


            description = elements[0].text.strip()



    except Exception as e:


        print(
            "Description error:",
            e
        )



    return description





# Compatibility function
# Used by description_loader.py

def extract_job_description(driver, url):

    return extract_job_details(
        driver,
        url
    )







# ==================================================
# LinkedIn Scraper
# ==================================================

def scrape_linkedin(

    keyword="Demand Planner",

    location="Dubai",

    pages=5,

    driver=None

):


    print(
        f"Searching LinkedIn: {keyword} - {location}"
    )



    jobs = []


    own_driver = False



    if driver is None:


        driver = create_driver()

        own_driver = True




    seen = set()



    try:



        for page in range(pages):


            start = page * 25



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
                "Page:",
                page + 1
            )



            driver.get(
                url
            )



            try:


                WebDriverWait(

                    driver,

                    15

                ).until(


                    EC.presence_of_all_elements_located(

                        (

                            By.CLASS_NAME,

                            "base-search-card"

                        )

                    )

                )


            except Exception:


                print(
                    "No cards found"
                )


                continue




            time.sleep(3)



            cards = driver.find_elements(

                By.CLASS_NAME,

                "base-search-card"

            )



            print(

                "Cards:",

                len(cards)

            )




            for card in cards:


                try:


                    title = card.find_element(

                        By.CLASS_NAME,

                        "base-search-card__title"

                    ).text.strip()



                    company = card.find_element(

                        By.CLASS_NAME,

                        "base-search-card__subtitle"

                    ).text.strip()



                    location_text = card.find_element(

                        By.CLASS_NAME,

                        "job-search-card__location"

                    ).text.strip()



                    link = card.find_element(

                        By.TAG_NAME,

                        "a"

                    ).get_attribute(

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



                    seen.add(
                        key
                    )



                    jobs.append(

                        {

                            "job_title": title,

                            "company": company,

                            "location": location_text,

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





        print(

            "Total collected:",

            len(jobs)

        )





        # Load descriptions

        for i, job in enumerate(jobs):


            print(

                f"Reading description {i+1}/{len(jobs)}"

            )


            job["description"] = extract_job_description(

                driver,

                job["url"]

            )



    except Exception as e:


        print(
            "LinkedIn scraper error:",
            e
        )



    finally:


        if own_driver:


            driver.quit()



    return jobs