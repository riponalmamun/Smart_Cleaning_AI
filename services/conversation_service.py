# services/conversation_service.py
import sqlite3
from datetime import datetime

DB_PATH = "conversations.db"

# -----------------------------
# Initialize the database
# -----------------------------
def init_db():
    """
    Create the conversations table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# -----------------------------
# Save a message
# -----------------------------
def save_message(user_email: str, message: str):
    """
    Save a user or bot message to the database.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (user_email, message) VALUES (?, ?)",
        (user_email, message)
    )
    conn.commit()
    conn.close()


# -----------------------------
# Get all messages for a user (WITH LIMIT PARAMETER)
# -----------------------------
def get_user_messages(user_email: str, limit: int = None):
    """
    Retrieve conversation messages for a user in chronological order.
    Returns a list of dictionaries: [{"message": str, "timestamp": str}, ...]
    
    :param user_email: User's email address
    :param limit: Maximum number of messages to return (optional)
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    
    if limit:
        c.execute(
            "SELECT message, timestamp FROM conversations WHERE user_email=? ORDER BY timestamp DESC LIMIT ?",
            (user_email, limit)
        )
        rows = c.fetchall()
        rows.reverse()  # Reverse to get chronological order
    else:
        c.execute(
            "SELECT message, timestamp FROM conversations WHERE user_email=? ORDER BY timestamp",
            (user_email,)
        )
        rows = c.fetchall()
    
    conn.close()
    return [{"message": r[0], "timestamp": r[1]} for r in rows]


# -----------------------------
# Get current conversation only (NEW FUNCTION)
# -----------------------------
def get_current_conversation(user_email: str, limit: int = None):
    """
    Get only the current ongoing conversation (after last booking completion).
    Filters out completed bookings and internal state messages.
    
    :param user_email: User's email address
    :param limit: Maximum number of messages to return (optional)
    :return: List of messages in current conversation
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    
    # Get all messages in reverse order (newest first)
    c.execute(
        "SELECT message, timestamp FROM conversations WHERE user_email=? ORDER BY timestamp DESC",
        (user_email,)
    )
    rows = c.fetchall()
    conn.close()
    
    # Find the current conversation (after last BOOKING_CONFIRMED or BOOKING_CANCELLED)
    current_conv = []
    for row in rows:
        message, timestamp = row
        
        # Stop at last completed/cancelled booking (but include it)
        if "BOOKING_CONFIRMED" in message or "BOOKING_CANCELLED" in message:
            # Include the confirmation message itself
            if "Bot:" in message:
                current_conv.append({"message": message, "timestamp": timestamp})
            break
        
        # Skip internal state messages from display
        if not any(x in message for x in ["PENDING_APPOINTMENT:", "SELECTED_SERVICE:", "BOOKING_CONFIRMED", "BOOKING_CANCELLED"]):
            current_conv.append({"message": message, "timestamp": timestamp})
    
    # Reverse to get chronological order
    current_conv.reverse()
    
    # Apply limit if specified
    if limit and len(current_conv) > limit:
        current_conv = current_conv[-limit:]
    
    return current_conv


# -----------------------------
# Clear conversation history for a user
# -----------------------------
def clear_conversation(user_email: str):
    """
    Clear all conversation history for a specific user.
    Useful for testing or allowing users to start fresh.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE user_email=?", (user_email,))
    conn.commit()
    conn.close()


# -----------------------------
# Initialize DB at import
# -----------------------------
init_db()