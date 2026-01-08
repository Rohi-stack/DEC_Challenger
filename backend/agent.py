from backend.databases import get_steps, save_notification
from openai import OpenAI
import os


class GoalPlanner:
    def plan(self, text: str):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"Break this goal into steps:\n{text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        steps_text = response.choices[0].message.content

        steps = steps_text.split("\n")

        return steps


class GoalExecutor:
    def execute(self, goal_id: int):

        steps = get_steps(goal_id)

        for s in steps:
            pass

        return True
