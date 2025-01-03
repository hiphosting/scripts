import argparse
import json
import requests
import time


def send_post_request(url, application_name, username, password, extra):
    # Prepare the payload
    payload = {
        "application_name": application_name,
        "username": username,
        "password": password,
    }

    # Add extra JSON if provided
    if extra:
        try:
            extra_data = json.loads(extra)
            payload["extra"] = extra_data
        except json.JSONDecodeError:
            print("Error: 'extra' argument must be a valid JSON string.")
            return

    # Retry logic
    attempts = 0
    success = False

    while attempts < 10:
        try:
            response = requests.post(url, json=payload)
            print(
                "Attempt", attempts + 1, "- Response Status Code:", response.status_code
            )

            if response.ok:
                success = True
                print("Response Body:", response.text)
                return
        except requests.RequestException as e:
            print("Attempt", attempts + 1, "- Error while sending POST request:", e)

        attempts += 1
        time.sleep(1)

    # If not successful after 10 attempts, retry every 10 seconds for 1 minute
    retry_attempts = 0
    while not success and retry_attempts < 6:
        try:
            response = requests.post(url, json=payload)
            print(
                "Retry Attempt",
                retry_attempts + 1,
                "- Response Status Code:",
                response.status_code,
            )

            if response.ok:
                success = True
                print("Response Body:", response.text)
                return
        except requests.RequestException as e:
            print(
                "Retry Attempt",
                retry_attempts + 1,
                "- Error while sending POST request:",
                e,
            )

        retry_attempts += 1
        time.sleep(10)

    print("Failed to get a successful response after multiple attempts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send a POST request with named arguments."
    )
    parser.add_argument(
        "--url", required=True, help="The URL to send the POST request to."
    )
    parser.add_argument(
        "--application_name", required=True, help="The name of the application."
    )
    parser.add_argument("--username", required=True, help="The username.")
    parser.add_argument("--password", required=True, help="The password.")
    parser.add_argument(
        "--extra",
        required=False,
        help="Additional JSON data as a string.",
        default="{}",
    )

    args = parser.parse_args()

    send_post_request(
        url=args.url,
        application_name=args.application_name,
        username=args.username,
        password=args.password,
        extra=args.extra,
    )
