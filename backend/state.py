from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    event_type: Optional[str]
    event_payload: Dict[str, Any]
    decision: Optional[Dict[str, Any]]
    action_result: Optional[Dict[str, Any]]
    memory_entry: Optional[Dict[str, Any]]
