from fastapi import FastAPI
from graph import agent_graph

app = FastAPI()

@app.post("/goal")
async def goal(req: dict):

    state = {
        "event_type": "goal",
        "event_payload": req,
        "decision": None,
        "action_result": None,
        "memory_entry": None
    }

    result = agent_graph.invoke(state)

    return {
        "goal_id": "simulated-id",
        "logs": result.get("logs", []),
        "decision": result.get("decision"),
        "result": result.get("action_result")
    }

@app.get("/status/{goal_id}")
async def status(goal_id: str):
    return {"status": "pending", "goal_id": goal_id}


@app.get("/")
async def root():
    return {
        "message": "Agent backend is running",
        "available_endpoints": ["/goal", "/status/{goal_id}"]
    }
