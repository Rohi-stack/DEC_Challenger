### DEC_Challenger

 ## INTRODUCTION 
 An Autonomous AI Agent designed to help users manage meetings, reminders, and career opportunities with minimal human input.
This agent automatically summarizes Google Meet sessions, sends emails, sets meeting reminders, and tracks internship & job notifications from platforms like LinkedIn.


## 🚀 Features
# 1. Google Meet Summary Automation

Fetches Google Meet transcripts

Uses LLM (OpenAI / other) to generate concise summaries

Automatically emails the summary to the user

# 2. Smart Meeting Reminders

Reads Google Calendar events

Sends reminders to the host before the meeting starts

Prevents missed or delayed meetings

# 3. Internship & Job Notification Alerts

Tracks internship/job notifications (LinkedIn & other platforms) ongoing 

Filters relevant opportunities

Sends email alerts to the user

# 4. Autonomous Task Execution

Works with minimal human intervention

Runs on scheduled background jobs

Decision-making handled by AI agent logic

🛠️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/ai-productivity-agent.git
cd ai-productivity-agent

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate # Linux / Mac
venv\Scripts\activate # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables

Create a .env file:

OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_password

▶️ Run the Project
uvicorn main:app --reload

Open browser:

http://127.0.0.1:8000
