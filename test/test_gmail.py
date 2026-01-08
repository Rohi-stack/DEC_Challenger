import asyncio
from backend.tools.gmail import send_email_gmail

print("Running Gmail tool test")

token = input("Paste Google OAuth access token: ")

recipients = ["someone@gmail.com"]

async def run():
    r = await send_email_gmail(
        token,
        recipients,
        "Test Mail",
        "Hello from backend test folder"
    )
    print("Result:", r)

asyncio.run(run())
