import os

from accuracy_validation_node.runner import (
    run_accuracy_validation
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

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    model = "gpt-4.1"

    temperature = 0.2

    original_project_root = (
        r"C:\Users\acer\Downloads\Nithiya_poc\HVAC"
    )

    remediated_project_root = (
        r"C:\Users\acer\Downloads\Nithiya_poc\workspace\remediated_project"
    )

    analysis_report_path = os.path.join(

        "analysis_reports",

        "final_analysis_report.json"

    )

    # --------------------------------------------------
    # Check Inputs
    # --------------------------------------------------

    if not os.path.exists(
        original_project_root
    ):

        print(
            "Original Project not found."
        )

        return

    if not os.path.exists(
        remediated_project_root
    ):

        print(
            "Remediated Project not found."
        )

        return

    if not os.path.exists(
        analysis_report_path
    ):

        print(
            "Analysis Report not found."
        )

        return

    # --------------------------------------------------
    # Run Accuracy Validation
    # --------------------------------------------------

    report = run_accuracy_validation(

        api_key=api_key,

        model=model,

        temperature=temperature,

        original_project_root=original_project_root,

        remediated_project_root=remediated_project_root,

        analysis_report_path=analysis_report_path

    )

    # --------------------------------------------------
    # Print Summary
    # --------------------------------------------------

    print()

    print("=" * 70)
    print("FINAL ACCURACY REPORT")
    print("=" * 70)

    summary = report["summary"]

    metrics = report["metrics"]

    print(
        f"Total Suggested Fixes : "
        f"{summary['total_suggested_fixes']}"
    )

    print(
        f"Implemented : "
        f"{summary['implemented']}"
    )

    print(
        f"Partially Implemented : "
        f"{summary['partially_implemented']}"
    )

    print(
        f"Not Implemented : "
        f"{summary['not_implemented']}"
    )

    print()

    print(
        f"Accuracy : "
        f"{metrics['accuracy_percent']} %"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()