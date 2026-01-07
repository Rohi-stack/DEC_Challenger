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