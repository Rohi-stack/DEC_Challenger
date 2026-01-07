def create_event(title, time):
    return {
        "tool": "calendar",
        "action": "event created",
        "title": title,
        "time": time
    }
