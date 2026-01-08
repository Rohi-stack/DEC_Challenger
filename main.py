from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.databases import get_notifications, mark_notification_read

from backend.models import MessageRequest, GoalRequest, TranscriptRequest
from backend.graph import agent_graph
from backend.databases import init_db, get_notifications
from backend.databases import (
    init_db,
    save_to_db,
    get_all_messages,
    save_goal,
    save_steps,
    get_steps
)
from backend.agent import GoalPlanner, GoalExecutor

app = FastAPI()

# ✅ CORS goes HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database once at startup
init_db()

planner = GoalPlanner()
executor = GoalExecutor()

@app.get("/")
def home():
    return {"status": "Backend Server Running"}

@app.post("/message")
def store_message(msg: MessageRequest):
    save_to_db(msg.text)
    return {"status": "ok", "message": msg.text}

@app.get("/messages")
def list_messages():
    data = get_all_messages()
    return {"count": len(data), "items": data}

@app.post("/goal")
def create_goal(goal: GoalRequest):

    steps = planner.plan(goal.text)

    goal_id = save_goal(goal.text)
    save_steps(goal_id, steps)

    return {
        "status": "stored",
        "goal_id": goal_id,
        "steps": steps
    }

@app.get("/steps/{goal_id}")
def show_steps(goal_id: int):
    data = get_steps(goal_id)
    return {
        "goal_id": goal_id,
        "items": data
    }

@app.post("/execute/{goal_id}")
def execute_goal(goal_id: int):

    executor.execute(goal_id)

    return {
        "status": "executed",
        "goal_id": goal_id
    }


from backend.graph import agent_graph

@app.post("/transcript")
async def receive_transcript(req: TranscriptRequest):

    state = {
        "event_type": "meeting_transcript",
        "event_payload": {
            "goal_id": req.goal_id,
            "transcript": req.transcript,
            "attendees": req.attendees,
            "access_token": req.access_token
        },
        "decision": None,
        "action_result": None,
        "memory_entry": None
    }

    result = agent_graph.invoke(state)

    return {
        "status": "processed",
        "goal_id": req.goal_id,
        "decision": result.get("decision"),
        "notification": result.get("action_result")
    }


from backend.databases import get_notifications

@app.get("/notifications")
def list_notifications():
    data = get_notifications()
    return {
        "count": len(data),
        "items": data
    }


@app.get("/notifications")
def list_notifications():
    data = get_notifications()
    return {
        "count": len(data),
        "items": data
    }


@app.post("/notifications/{notification_id}/read")
def read_notification(notification_id: int):
    mark_notification_read(notification_id)
    return {"status": "ok"}