
from fastapi import FastAPI
# from models import MessageRequest
# from models import MessageRequest
from backend.models import MessageRequest
from backend.models import GoalRequest
from backend.models import MessageRequest

# from database import save_to_db
from backend.databases import save_to_db, get_all_messages



app = FastAPI()

@app.post("/message")
def store_message(msg: MessageRequest):

    save_to_db(msg.text)

    return {
        "status": "ok",
        "message": msg.text
    }






@app.get("/messages")
def list_messages():

    data = get_all_messages()

    return {
        "count": len(data),
        "items": data
    }



@app.post("/goal")
def create_goal(goal: GoalRequest):
    # call OpenAI API here to generate steps
    return {"goal_id": 1}

@app.get("/")
def home():
    return {"status": "Backend Server Running"}


from backend.agent import GoalPlanner


planner = GoalPlanner()

@app.post("/goal")
def create_goal(goal: GoalRequest):
    steps = planner.plan(goal.text)
    return {"steps": steps}
