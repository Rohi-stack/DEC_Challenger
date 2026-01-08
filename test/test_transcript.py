import requests
import json

print("Running /transcript integration test")

BASE_URL = "http://127.0.0.1:8000/transcript"

# Paste a VALID OAuth access token here when prompted
access_token = input("Paste Google OAuth access token: ").strip()

payload = {
    "goal_id": "test-meeting-001",
    "transcript": """
Aryan: Let's quickly sync.
Rahul: The backend integration is almost done.
Aryan: We need to email the summary to everyone.
Rahul: Yes, and add notifications on homepage.
""",
    "attendees": [
        "aryan.prasad1897@gmail.com"
    ],
    "access_token": access_token
}

try:
    response = requests.post(
        BASE_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30
    )

    print("HTTP Status:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

except Exception as e:
    print("Test failed:", str(e))
