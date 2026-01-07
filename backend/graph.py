from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from state import AgentState
from prompts import DECISION_PROMPT

import dotenv
dotenv.load_dotenv()


llm = ChatOpenAI(model="gpt-4o", temperature=0)

def observe(state: AgentState):
    return state

def decide(state: AgentState):

    prompt = DECISION_PROMPT.format(
        event_type=state["event_type"],
        event_payload=state["event_payload"]
    )

    response = llm.invoke(prompt)

    import json
    try:
        state["decision"] = json.loads(response.content)
    except:
        state["decision"] = {"action": "no_action", "reason": "invalid response"}

    return state

def act(state: AgentState):

    action = state["decision"]["action"]

    if action == "summarize_meeting":
        state["action_result"] = {"status": "meeting summarized"}

    elif action == "classify_job_email":
        state["action_result"] = {"status": "job email classified"}

    elif action == "notify_user":
        state["action_result"] = {"status": "user notified"}

    else:
        state["action_result"] = {"status": "no action"}

    return state


graph = StateGraph(AgentState)

graph.add_node("observe", observe)
graph.add_node("decide", decide)
graph.add_node("act", act)

graph.set_entry_point("observe")

graph.add_edge("observe", "decide")
graph.add_edge("decide", "act")
graph.add_edge("act", END)

agent_graph = graph.compile()
