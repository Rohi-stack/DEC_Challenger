import sqlite3

def save_to_db(text):

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
    )

    cursor.execute(
        "INSERT INTO messages (text) VALUES (?)", (text,)
    )

    conn.commit()
    conn.close()

    return True


def get_all_messages():

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM messages")
    rows = cursor.fetchall()

    conn.close()

    return rows

from datetime import datetime

def init_db():

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,
            step_text TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)

    conn.commit()
    conn.close()

def save_steps(goal_id, steps):

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()

    for s in steps:
        if s.strip():
            cursor.execute(
                "INSERT INTO steps (goal_id, step_text, status) VALUES (?, ?, 'PENDING')",
                (goal_id, s)
            )

    conn.commit()
    conn.close()

    return True


def get_steps(goal_id):

    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, step_text, status FROM steps WHERE goal_id = ?",
        (goal_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows



# save_goal(text)
def save_goal(text):
    conn = sqlite3.connect("agent.db")
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("INSERT INTO goals (text, created_at) VALUES (?, ?)", (text, now))
    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return goal_id



# save_steps(goal_id, steps)

# Inside databases.py, add:

# goals table

# steps table with goal_id foreign key

