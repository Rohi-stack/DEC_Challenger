from langchain_openai import ChatOpenAI
import os
import json
from backend.config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

SUMMARIZE_PROMPT = """
You are an expert meeting summarization AI.

Transcript:
{transcript}

Return a concise professional summary.
"""

def summarize(transcript: str):

    response = llm.invoke(SUMMARIZE_PROMPT.format(transcript=transcript))

    return {
        "summary": response.content,
        "status": "success"
    }
