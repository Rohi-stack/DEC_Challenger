from pydantic import BaseModel

class MessageRequest(BaseModel):
    text: str

class GoalRequest(BaseModel):
    text: str



# Add a schema to represent goals and steps.

# For example:

# GoalCreate

# StepResponse

# This keeps your API contracts clean.