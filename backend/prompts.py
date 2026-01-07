DECISION_PROMPT = """
You are an autonomous AI agent.

Event Type: {event_type}
Event Payload: {event_payload}

Decide the next action.

Possible actions:
- summarize_meeting
- send_meeting_reminder
- classify_job_email
- notify_user
- no_action

Respond ONLY in JSON:
{
  "action": "<action_name>",
  "reason": "short explanation"
}
"""
