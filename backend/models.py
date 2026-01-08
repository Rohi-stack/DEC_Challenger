from typing import List
from pydantic import BaseModel


class MessageRequest(BaseModel):
    text: str


class GoalRequest(BaseModel):
    text: str


class TranscriptRequest(BaseModel):
    goal_id: str
    transcript: str
    attendees: List[str]
    access_token: str

# Add a schema to represent goals and steps.

# For example:

# GoalCreate

# StepResponse

# This keeps your API contracts clean.