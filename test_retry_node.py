from retry_compilation_node.retry_runner import (
    run_retry_node
)


def main():

    api_key = input(
        "Enter OpenAI API Key: "
    )

    if not api_key.strip():

        print(
            "API Key cannot be empty"
        )

        return

    result = run_retry_node(
        api_key=api_key,
        model="gpt-4.1"
    )

    print("\n")
    print("=" * 60)
    print("RETRY TASK SUMMARY")
    print("=" * 60)

    print(
        f"Build Status : "
        f"{result['build_status']}"
    )

    print(
        f"Error Count : "
        f"{result['error_count']}"
    )

    print(
        f"Warning Count : "
        f"{result['warning_count']}"
    )

    print(
        f"Files Identified : "
        f"{result['files_identified']}"
    )

    print(
        f"Files Fixed : "
        f"{result['files_fixed']}"
    )

    print(
        f"Files Failed : "
        f"{result['files_failed']}"
    )

    print("=" * 60)

    if result["retry_tasks"]:

        print("\nPROCESSED FILE DETAILS")
        print("=" * 60)

        for idx, task in enumerate(
            result["retry_tasks"],
            start=1
        ):

            print(
                f"\n[{idx}] File : "
                f"{task['file']}"
            )

            print(
                f"Actual Path : "
                f"{task['actual_path']}"
            )

            print(
                f"Errors : "
                f"{task['error_count']}"
            )

            print(
                f"Source Length : "
                f"{len(task['source_code'])}"
            )

            print("-" * 60)

    else:

        print(
            "\nNo files were successfully processed."
        )


if __name__ == "__main__":
    main()