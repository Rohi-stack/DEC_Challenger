from backend.tools.summarizer import summarize


print("Running summarizer test")

sample_transcript = """
Host: Backend architecture discussed.
Aryan: Testing pipeline.
Attendee: Email integration planned.
"""

result = summarize(sample_transcript)

print("Summary:", result)
