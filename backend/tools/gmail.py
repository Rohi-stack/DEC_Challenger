import httpx
import base64
from email.mime.text import MIMEText


async def send_email_gmail(access_token: str, to_list: list, subject: str, body: str):

    # Create proper MIME formatted email
    message = MIMEText(body)
    message["to"] = ", ".join(to_list)
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers=headers,
            json={"raw": raw}
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "message": response.text
            }

    return {"status": "emails dispatched"}
