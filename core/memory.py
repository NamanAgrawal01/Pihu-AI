from database.database import (
    save_memory,
    get_memory,
    save_chat,
    connect
)


def remember(key, value):
    save_memory(key, value)


def recall(key):
    return get_memory(key)


def remember_conversation(user, ai):
    save_chat(user, ai)
def get_history(username): # Ab username argument mangenge
    conn = connect()
    cur = conn.cursor()

    # Sirf us user ka data fetch karenge
    cur.execute("""
        SELECT user, assistant
        FROM chat_history
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 20
    """, (username,)) # yahan username pass karenge

    rows = cur.fetchall()
    conn.close()

    history = []
    for user, assistant in reversed(rows):
        history.append({
            "user": user,
            "assistant": assistant
        })
    return history