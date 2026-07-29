import json
import os
from datetime import datetime


TRACKER_FILE = "data/applications/applications.json"


def load_applications():

    if not os.path.exists(TRACKER_FILE):
        return []

    with open(
        TRACKER_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_applications(applications):

    os.makedirs(
        "data/applications",
        exist_ok=True
    )

    with open(
        TRACKER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            applications,
            file,
            indent=2,
            ensure_ascii=False
        )



def add_application():

    applications = load_applications()

    print("\nAdd New Application\n")


    application = {

        "company":
        input("Company: "),


        "job_title":
        input("Job Title: "),


        "location":
        input("Location: "),


        "url":
        input("Job URL: "),


        "match_score":
        input("Match Score: "),


        "status":
        input(
            "Status (Saved/Applied/Interview/Offer/Rejected): "
        ),


        "application_date":
        str(datetime.now().date()),


        "follow_up":
        input("Follow-up date: "),


        "notes":
        input("Notes: ")

    }


    applications.append(
        application
    )


    save_applications(
        applications
    )


    print(
        "\nApplication saved successfully"
    )



def view_applications():

    applications = load_applications()


    if not applications:

        print(
            "\nNo applications found"
        )

        return


    print(
        "\nAPPLICATION TRACKER\n"
    )


    for index, app in enumerate(applications, 1):

        print(
            f"""
{index}. {app['company']}
Role: {app['job_title']}
Location: {app['location']}
Score: {app['match_score']}
Status: {app['status']}
Applied: {app['application_date']}
Follow-up: {app['follow_up']}
Notes: {app['notes']}
-----------------------------
"""
        )



def update_status():

    applications = load_applications()


    view_applications()


    if not applications:
        return


    number = int(
        input("Select application number: ")
    )


    status = input(
        "New status: "
    )


    applications[number-1]["status"] = status


    save_applications(
        applications
    )


    print(
        "Status updated"
    )



def main():

    while True:

        print(
            """
========================
AI Career Agent Tracker
========================

1. Add Application
2. View Applications
3. Update Status
4. Exit
"""
        )


        choice = input(
            "Choose: "
        )


        if choice == "1":

            add_application()


        elif choice == "2":

            view_applications()


        elif choice == "3":

            update_status()


        elif choice == "4":

            break


        else:

            print(
                "Invalid choice"
            )



if __name__ == "__main__":

    main()