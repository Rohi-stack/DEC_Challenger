from fastapi import FastAPI
from backend.models import MessageRequest, GoalRequest
from backend.databases import save_to_db, get_all_messages, init_db
from backend.agent import GoalPlanner
from backend.databases import (
    save_goal,
    save_steps,
    get_steps,
    save_to_db,
    get_all_messages,
    init_db
)

app = FastAPI()

init_db()

planner = GoalPlanner()

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
    return {"goal_id": goal_id, "items": data}


from backend.agent import GoalExecutor
executor = GoalExecutor()

@app.post("/execute/{goal_id}")
def execute_goal(goal_id: int):

    result = executor.execute(goal_id)

    return {
        "status": "executed",
        "goal_id": goal_id
    }

from backend.agent import GoalExecutor
executor = GoalExecutor()

@app.post("/execute/{goal_id}")
def execute_goal(goal_id: int):

    result = executor.execute(goal_id)

    return {
        "status": "executed",
        "goal_id": goal_id
    }
# POST /execute/{goal_id}
