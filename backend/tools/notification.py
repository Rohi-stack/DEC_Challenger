def send_notification(text):
    return {
        "tool": "notification",
        "action": "notified user",
        "text": text
    }
