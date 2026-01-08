import asyncio
from backend.graph import decide, act

state = {
    "event_type": "goal",
    "event_payload": {
        "text": "Test goal processing",
        "transcript": "Aryan: Test transcript for graph.",
        "attendees": [],
        "access_token": ""
    },
    "decision": None,
    "action_result": None,
    "memory_entry": None
}

print("Testing decide node")
print(decide(state))

print("Testing act node")

async def run():
    print(await act(state))

asyncio.run(run())
