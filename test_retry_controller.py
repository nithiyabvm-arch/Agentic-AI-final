import os

from retry_compilation_node.retry_controller import (
    run_retry_cycle
)

api_key = os.getenv(
    "OPENAI_API_KEY"
)

if not api_key:

    print(
        "OPENAI_API_KEY not found"
    )

else:

    result = run_retry_cycle(
        api_key=api_key,
        model="gpt-4.1",
        max_retries=10
    )

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(
        f"Build Status : "
        f"{result['build_status']}"
    )

    print(
        f"Attempts : "
        f"{result['attempts']}"
    )

    print(
        f"Final Errors : "
        f"{result['final_error_count']}"
    )