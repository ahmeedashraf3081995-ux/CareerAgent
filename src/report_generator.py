def generate_report(job, result):

    print("\n==========================")
    print(f"{job['company']} - {job['title']}")
    print("==========================")

    print(f"Location: {job['location']}")
    print(f"Match Score: {result['overall_score']}")

    print("\nMatched Skills:")
    for skill in result["matched_skills"]:
        print(f"✓ {skill}")

    print("\nMissing Skills:")
    if result["missing_skills"]:
        for skill in result["missing_skills"]:
            print(f"✗ {skill}")
    else:
        print("None")

    print("\nRecommendation:")
    print(result["recommendation"])

    print("==========================")