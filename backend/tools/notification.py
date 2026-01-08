async def create_notification(goal_id: str, summary: str):

    return {
        "goal_id": goal_id,
        "message": summary,
        "status": "created"
    }
