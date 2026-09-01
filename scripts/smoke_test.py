import os
import sys

import httpx


def main() -> int:
    base_url = os.environ["STAGING_APP_URL"].rstrip("/")
    timeout = float(os.getenv("SMOKE_TIMEOUT_SECONDS", "20"))

    with httpx.Client(timeout=timeout) as client:
        health = client.get(f"{base_url}/health")
        health.raise_for_status()

        response = client.post(
            f"{base_url}/invocations",
            json={"message": "What tier is $225/night?"},
        )
        response.raise_for_status()
        body = response.json()

    if not body.get("answer"):
        print("Smoke test failed: empty answer")
        return 1

    print("Smoke test passed")
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
