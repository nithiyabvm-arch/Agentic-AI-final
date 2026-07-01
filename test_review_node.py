import json

from review_node.review_runner import (
    run_review
)


def main():

    report = run_review()

    print("\n")
    print("=" * 60)
    print("REVIEW REPORT")
    print("=" * 60)

    print(
        json.dumps(
            report,
            indent=4
        )
    )


if __name__ == "__main__":
    main()