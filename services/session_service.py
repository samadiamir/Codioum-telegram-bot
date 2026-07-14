from datetime import datetime, timezone
from utils.database import get_connection
from utils.logger import log_debug, log_error, log_info
from utils.constants import Emojis
from services.ai_service import get_ai_response


def create_session(user_id : int, first_message=None):
    """Create a new session for a user and return its ID."""
    session_name = "New Chat"
    utc_time = datetime.now(timezone.utc).isoformat() + "Z"
    
    conn = get_connection()
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for creating session.")
        return None
    
    try:
        cursor = conn.cursor()
        log_debug(f"{Emojis.SESSIONS} Creating session for user {user_id}")
        
        cursor.execute("""
            INSERT INTO sessions (user_id, name, created_at)
            VALUES (?, ?, ?)
        """, (user_id, session_name, utc_time))
        
        conn.commit()
        session_id = cursor.lastrowid
        log_info(f"{Emojis.SUCCESS} Session {session_id} created for user {user_id}")
        return session_id
        
    except Exception as e:
        log_error(f"{Emojis.ERROR} Failed to create session for user {user_id}", e)
        return None
    finally:
        conn.close()



def get_session_history(session_id: int) -> list:
    conn = get_connection()
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for getting session history.")
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
        history = cursor.fetchall()
        return [dict(row) for row in history]
        
    except Exception as e:
        log_error(f"{Emojis.ERROR} Failed to get session history", e)
        
    finally:
        conn.close()




def generate_session_name(first_message: str) -> str:
    prompt = f"""You are a session title generator. Your ONLY job is to return a short title (3-5 words max) for the following message. **Reply with ONLY the title**e. No explanation, no quotes, no extra text. Just the title itself.

Message: {first_message[:200]}"""

    try:
        title = get_ai_response(prompt)
        if title:
            title = title.strip().strip('"').strip("'").strip()
            return title
        return "New Chat"
        
    except Exception as response_error:
        log_error(f"{Emojis.ERROR} Failed to get ai response", response_error)
        return "New Chat"


def rename_session(session_id, new_name : str) -> None:
    """ Updating the name with ai in session table"""
    
    conn = get_connection()
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for creating session.")
        return None

    try:
        cursor = conn.cursor()

        log_debug(f"{Emojis.SESSIONS} Updating session name")
        cursor.execute("UPDATE sessions SET name = ? WHERE id = ?", (new_name, session_id))

        conn.commit()
        log_info(f"{Emojis.SUCCESS} Session {session_id} updated.")

    except Exception as update_error:
        log_error(f"{Emojis.ERROR} Failed to update session", update_error)
        return None
        
    finally:
        conn.close()




def get_user_sessions(user_id) -> list:
    
    log_debug(f"{Emojis.SESSIONS} Connecting to database for user {user_id}")
    conn = get_connection()
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for creating session.")
        return None
    try:
        cursor = conn.cursor()
        
        log_debug(f"{Emojis.SESSIONS} Selecting values from session table in database for user {user_id}")
        cursor.execute("SELECT id, name, created_at from sessions WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    except Exception as e:
        log_error(f"{Emojis.ERROR} Failed to select values for user {user_id}", e)
        return None
    finally:
        conn.close()