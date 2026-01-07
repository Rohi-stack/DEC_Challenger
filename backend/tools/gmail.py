def send_email(to, subject, body):
    return {
        "tool": "gmail",
        "action": "email sent",
        "to": to,
        "subject": subject
    }
