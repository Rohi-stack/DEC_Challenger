from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from backend.state import AgentState
import sqlite3
import json
import os

# from backend.databases import save_notification
from backend.tools.summarizer import summarize
from backend.tools.gmail import send_email_gmail
from backend.tools.notification import create_notification

from backend.databases import save_notification


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def decide(state: AgentState):

    if state["event_type"] == "meeting_transcript":
        state["decision"] = {
            "steps": [
                {"action": "summarize_meeting"},
                {"action": "send_email"}
            ]
        }
        return state

    # existing goal-planning logic below (unchanged)

def act(state: AgentState):

    payload = state["event_payload"]

    goal_id = payload.get("goal_id")
    transcript = payload.get("transcript")
    access_token = payload.get("access_token")
    attendees = payload.get("attendees", [])

    print("Transcript processed for goal:", goal_id)

    # Call summarizer (sync-safe handling)
    result = summarize(transcript)
    if hasattr(result, "__await__"):
        result = result.send(None)

    summary_text = result["summary"]

    save_notification(goal_id, summary_text)


    send_email_gmail(
        access_token,
        attendees,
        "Meeting Summary",
        summary_text
    )

    save_notification(goal_id, summary_text)
    state["action_result"] = {
        "goal_id": goal_id,
        "message": summary_text
    }

    return state



graph = StateGraph(AgentState)

graph.add_node("decide", decide)
graph.add_node("act", act)

graph.set_entry_point("decide")

graph.add_edge("decide", "act")
graph.add_edge("act", END)

agent_graph = graph.compile()
