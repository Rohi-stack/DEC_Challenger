### DEC_Challenger

# Hackathon PPA – Productivity & Meeting Assistant

Hackathon PPA is an end-to-end **AI-powered productivity assistant** that integrates with **Google Meet, Google Calendar, and Gmail** to automatically:

- Capture meeting transcripts
- Generate structured meeting summaries using LLMs
- Email summaries to all attendees
- Show real-time notifications on a dashboard
- Track goals, steps, and meeting actions

This project is designed as a **modular, event-driven system** with a clean separation between:
- Data capture (Chrome Extension)
- Intelligence & orchestration (Backend + LangGraph)
- User interaction (Frontend Dashboard)

---

## 🧠 Core Features

- ✅ Google Meet transcript ingestion
- ✅ AI-powered meeting summarization
- ✅ Automatic email dispatch to attendees
- ✅ Real-time notification system
- ✅ Goal planning & execution pipeline
- ✅ Clean API-driven backend
- ✅ Chrome Extension for automation
- ✅ Dark-mode dashboard UI

---

## 🏗️ Project Architecture

Chrome Extension
↓
POST /transcript
↓
LangGraph (decide → act)
↓
Summarize → Email → Save Notification
↓
Frontend Dashboard (Notifications + Recent Summary)

yaml
Copy code

---

## 📁 Project Structure

DECHack/
├── backend/
│ ├── tools/ # summarizer, gmail, calendar, notification tools
│ ├── agent.py # GoalPlanner & GoalExecutor
│ ├── graph.py # LangGraph orchestration
│ ├── databases.py # SQLite persistence layer
│ ├── models.py # Pydantic schemas
│ ├── state.py # AgentState definition
│ └── config.py # Environment configuration
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
│
├── extension/ # Chrome Extension (Meet integration)
│ ├── manifest.json
│ ├── content.js
│ ├── background.js
│ └── popup.html
│
├── test/ # End-to-end & unit tests
│ ├── test_db.py
│ ├── test_summarizer.py
│ ├── test_gmail.py
│ ├── test_calendar.py
│ ├── test_notifications.py
│ └── test_transcript.py
│
├── main.py # FastAPI entrypoint
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Tech Stack

- **Backend**: FastAPI, LangGraph, LangChain
- **LLM**: OpenAI (via langchain-openai)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Vanilla JS
- **Extension**: Chrome Extension (Manifest V3)
- **Auth**: Google OAuth 2.0
- **Testing**: Python test scripts

---

## 🔐 Environment Setup

Create a `.env` file (do NOT commit it):

```env
OPENAI_API_KEY=your_openai_key_here
Make sure .env is listed in .gitignore.

📦 Installation
1️⃣ Clone repository
bash
Copy code
git clone https://github.com/Rohi-stack/DEC_Challenger.git
cd DECHack
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Start backend server
bash
Copy code
uvicorn main:app --reload
Backend runs at:

cpp
Copy code
http://127.0.0.1:8000
🖥️ Frontend Usage
Open frontend/index.html using Live Server (VS Code recommended):

cpp
Copy code
http://127.0.0.1:5500
Features:

Google Sign-In

Command input (e.g., “create meeting”)

Notification bell with unread count

Recent meeting summary display

🧩 Chrome Extension Setup
Open Chrome → chrome://extensions

Enable Developer Mode

Click Load unpacked

Select the extension/ folder

The extension:

Reads live captions from Google Meet

Sends transcript to backend /transcript

Triggers summary + email + notification pipeline

🔁 Workflow Example
User joins a Google Meet

Chrome Extension captures captions

Transcript is sent to backend:

bash
Copy code
POST /transcript
LangGraph decides actions:

summarize_meeting

send_email

Summary is generated

Emails sent to attendees

Notification stored in DB

Dashboard updates in real time

🧪 Testing
Run tests individually (recommended):

bash
Copy code
PYTHONPATH=. python test/test_db.py
PYTHONPATH=. python test/test_summarizer.py
PYTHONPATH=. python test/test_gmail.py
PYTHONPATH=. python test/test_transcript.py
🚀 Why This Project Matters
This is not a demo script — it is a production-style AI system that demonstrates:

Event-driven agent design

Tool-using LLM orchestration

Real OAuth + API integrations

Clean frontend-backend separation

Practical AI for real workflows

📌 Future Improvements
Automatic meeting end detection

Real-time transcript streaming

Multi-user dashboards

Production OAuth verification

Notification read/unread UX polish

👨‍💻 Authors
Built as part of a hackathon project by the DEC team.













ChatGPT can make mistakes. Check important info. See Cookie Preferences.
