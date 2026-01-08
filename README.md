# Productivity Assistant (Hackathon PPA)

Chrome Extension → **POST /transcript** → **LangGraph (decide → act)** → **Summarize → Email → Save Notification** → **Frontend Dashboard**

This project captures Google Meet transcripts via a Chrome extension, summarizes meetings using an LLM, emails the summary to attendees, and surfaces notifications and recent summaries in a frontend dashboard.

---

## ✨ Features

* 🔔 Notification bell with unread count
* 🧾 Recent meeting summary display
* 🧠 LangGraph-based agent (decide → act)
* ✉️ Automated email summaries to attendees
* 🧩 Chrome Extension (Manifest V3) for Google Meet captions
* 🗃️ SQLite persistence (messages, goals, steps, notifications)
* 🧪 End-to-end and unit tests

---

## 📁 Project Structure

```text
DECHack/
├── backend/
│   ├── tools/                 # summarizer, gmail, calendar, notification tools
│   ├── agent.py               # GoalPlanner & GoalExecutor
│   ├── graph.py               # LangGraph orchestration
│   ├── databases.py           # SQLite persistence layer
│   ├── models.py              # Pydantic schemas
│   ├── state.py               # AgentState definition
│   ├── config.py              # Environment configuration
│   └── __init__.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── extension/                 # Chrome Extension (Meet integration)
│   ├── manifest.json
│   ├── content.js
│   └── popup.html
├── test/                      # End-to-end & unit tests
│   ├── test_db.py
│   ├── test_summarizer.py
│   ├── test_gmail.py
│   ├── test_calendar.py
│   ├── test_notifications.py
│   └── test_transcript.py
├── main.py                    # FastAPI entrypoint
├── requirements.txt
└── README.md
```

---

## 🧰 Tech Stack

* **Backend**: FastAPI, LangGraph, LangChain
* **LLM**: OpenAI (via `langchain-openai`)
* **Database**: SQLite
* **Frontend**: HTML, CSS, Vanilla JavaScript
* **Extension**: Chrome Extension (Manifest V3)
* **Auth**: Google OAuth 2.0
* **Testing**: Python test scripts

---

## ⚙️ Environment Setup

Create a `.env` file **(do NOT commit this file)**:

```env
OPENAI_API_KEY=your_openai_key
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

---

## 🧪 Testing

Run tests from the project root:

```bash
PYTHONPATH=. python test/test_db.py
PYTHONPATH=. python test/test_summarizer.py
PYTHONPATH=. python test/test_gmail.py
PYTHONPATH=. python test/test_calendar.py
PYTHONPATH=. python test/test_notifications.py
PYTHONPATH=. python test/test_transcript.py
```

---

## 🧩 Chrome Extension Setup

1. Open Chrome → `chrome://extensions`
2. Enable **Developer Mode**
3. Click **Load unpacked**
4. Select the `extension/` folder

### What the extension does

* Reads live captions from Google Meet
* Sends transcript to backend `/transcript`
* Triggers summarize → email → notification pipeline

---

## 🔄 Workflow Example

1. User joins a Google Meet
2. Chrome Extension captures live captions
3. Transcript is sent to backend:

```http
POST /transcript
```

4. LangGraph decides actions:

* `summarize_meeting`
* `send_email`

5. Summary is generated
6. Emails are sent to attendees
7. Notification is stored in DB
8. Frontend dashboard updates (bell + recent summary)

---

## 🧭 Notes

* CORS is configured for local frontend (`127.0.0.1:5500`)
* OAuth tokens are requested client-side and passed securely
* All new features are additive and do not break existing flows

---

## 🚀 Next Improvements

* Mark notifications as read
* Meeting history page
* Chrome extension UI polish
* Export summaries (PDF / Docs)
* Slack or webhook integrations
* LinkedIn integration, updating user for new job postings
---

**Built for hackathon use with clarity, testability, and extensibility in mind.**
