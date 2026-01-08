def create_event(title: str, time: str):

    return {
        "tool": "calendar",
        "action": "event created",
        "title": title,
        "time": time
    }
