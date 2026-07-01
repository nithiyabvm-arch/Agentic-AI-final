import json

from analysis_review_node.review_runner import (
    run_analysis_review
)


def main():

    api_key = input(
        "Enter OpenAI API Key: "
    ).strip()

    if not api_key:

        print(
            "API Key cannot be empty."
        )

        return

    # -------------------------------------------------
    # Fixed Project Root
    # -------------------------------------------------

    project_root = (
        r"C:\Users\acer\Downloads\Nithiya_poc\HVAC"
    )

    # -------------------------------------------------
    # Fixed Context Path
    # -------------------------------------------------

    context_path = (
        r"C:\Users\acer\Downloads\Nithiya_poc\context.json"
    )

    try:

        with open(
            context_path,
            "r",
            encoding="utf-8"
        ) as f:

            project_context = json.load(f)

    except Exception as e:

        print(
            "\nUnable to load Project Context:"
        )

        print(e)

        return

    # -------------------------------------------------
    # Coding Guidelines
    # -------------------------------------------------

    guideline_path = input(
        "\nEnter Coding Guidelines JSON Path: "
    ).strip()

    if not guideline_path:

        print(
            "Guidelines path cannot be empty."
        )

        return

    try:

        with open(
            guideline_path,
            "r",
            encoding="utf-8"
        ) as f:

            coding_guidelines = json.load(f)

    except Exception as e:

        print(
            "\nUnable to load Guidelines:"
        )

        print(e)

        return

    # -------------------------------------------------
    # Run Analysis Review
    # -------------------------------------------------

    result = run_analysis_review(

        api_key=api_key,

        model="gpt-4.1",

        temperature=0.2,

        project_root=project_root,

        project_context=project_context,

        coding_guidelines=coding_guidelines

    )

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    print("\n")

    print("=" * 60)
    print("ANALYSIS REVIEW REPORT")
    print("=" * 60)

    summary = result["summary"]

    metrics = result["metrics"]

    print(
        f"Initial Issues : "
        f"{summary['initial_analysis_issues']}"
    )

    print(
        f"Additional Issues : "
        f"{summary['new_issues']}"
    )

    print(
        f"Total Issues : "
        f"{summary['second_analysis_issues']}"
    )

    print(
        f"Coverage : "
        f"{metrics['coverage_percent']} %"
    )

    print(
        f"Assessment : "
        f"{result['assessment']}"
    )

    print("=" * 60)

    print(
        "\nOutput File : analysis_review_reports/analysis_review_report.json"
    )


if __name__ == "__main__":
    main()