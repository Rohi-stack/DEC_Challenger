class GoalPlanner:
    def plan(self, text):
        # OpenAI API call
        return ["step1", "step2"]


from openai import OpenAI
import os

class GoalPlanner:
    def plan(self, text):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"Break this goal into clear actionable steps:\n{text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        steps_text = response.choices[0].message.content

        steps = steps_text.split("\n")

        return steps
