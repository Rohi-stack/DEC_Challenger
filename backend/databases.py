import sqlite3
from datetime import datetime

DB_PATH = "agent.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id TEXT,
            message TEXT,
            created_at TEXT,
            read INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_to_db(text: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO messages (text) VALUES (?)", (text,))

    conn.commit()
    conn.close()
    return True


def get_all_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, text FROM messages")
    rows = cursor.fetchall()

    conn.close()
    return rows


def save_goal(text: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO goals (text, created_at) VALUES (?, ?)",
        (text, datetime.utcnow().isoformat())
    )

    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return goal_id


def save_steps(goal_id: int, steps: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for s in steps:
        if s.strip():
            cursor.execute(
                "INSERT INTO steps (goal_id, step_text) VALUES (?, ?)",
                (goal_id, s)
            )

    conn.commit()
    conn.close()
    return True


def get_steps(goal_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, step_text, status FROM steps WHERE goal_id = ?",
        (goal_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def save_notification(goal_id: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notifications (goal_id, message, created_at, read) VALUES (?, ?, ?, 0)",
        (goal_id, message, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()


def get_notifications(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, goal_id, message, created_at, read
        FROM notifications
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_notification_read(notification_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notifications SET read = 1 WHERE id = ?",
        (notification_id,)
    )

    conn.commit()
    conn.close()
