"""
History management module.
Stores and manages per-user event history for AI chat, location sharing,
and other bot actions.
"""

from datetime import datetime
from utils.database import get_connection
from utils.logger import log_error, log_debug, log_warning



def get_user_history(user_id, event_types=None):
    """
    Get history events for a user.

    Args:
        user_id (int): The user's Telegram ID
        event_types (list|str|None): Optional event type filter

    Returns:
        list: List of history event dictionaries
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if not event_types:
            cursor.execute("SELECT user_id, event_type, role, content, timestamp FROM messages WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("SELECT user_id, event_type, role, content, timestamp FROM messages WHERE user_id = ? AND event_type = ?", (user_id, event_types,))
        results = cursor.fetchall()
        conn.close()
        
        return results
            
    except Exception as e:
        log_error(f"Error getting history for user {user_id}", e)
        return []


def add_history_event(user_id, event_type, content, role=None, metadata=None, session_id=None):
    """
    Add a generic history event for a user.

    Args:
        user_id (int): The user's Telegram ID
        event_type (str): Type of history event, e.g. 'ai_chat', 'location', 'action'
        content (str): Event content or description
        metadata (dict|None): Optional extra data
    """
    try:

        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": event_type,
            "content": content,
            "session_id": session_id
        }
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (user_id, role, content, event_type, timestamp, session_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, role, content, event_type, datetime.utcnow().isoformat() + "Z", session_id))
        conn.commit()
        conn.close()
        return event
    except Exception as e:
        log_error(f"Error adding history event for user {user_id}", e)
        return None

def add_message_to_history(user_id, role, content, session_id=None):
    """
    Add an AI chat message to user history.

    Args:
        user_id (int): The user's Telegram ID
        role (str): 'user' or 'assistant'
        content (str): Message content
    """
    try:
        if not role or not isinstance(role, str):
            raise ValueError(f"Invalid role: {role}")

        if role not in ["user", "assistant"]:
            log_warning(f"Unexpected role value: {role}")

        return add_history_event(user_id, "ai_chat", content, role, session_id=session_id)
    except Exception as e:
        log_error(f"Error adding message to history for user {user_id}", e)
        return None


def add_location_to_history(user_id, latitude, longitude, description=None):
    """
    Add a location sharing event to user history.

    Args:
        user_id (int): The user's Telegram ID
        latitude (float): Latitude value
        longitude (float): Longitude value
        description (str|None): Optional textual description
    """
    try:
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError(f"Invalid coordinates: {latitude}, {longitude}")

        content = description or f"Shared location ({latitude}, {longitude})"
        return add_history_event(
            user_id,
            "location",
            content,
            role=None,
            metadata= {"latitude": latitude, "longitude": longitude,}
        )
    except Exception as e:
        log_error(f"Error adding location to history for user {user_id}", e)
        return None


def clear_user_history(user_id, event_types=None):
    """
    Clear history events for a user.

    Args:
        user_id (int): The user's Telegram ID
        event_types (list|str|None): Optional event type filter. Clears all history if None.
    """
    try:
        
        conn = get_connection()
        cursor = conn.cursor()
        if not event_types:
            cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        else :
            cursor.execute("DELETE FROM messages WHERE user_id = ? AND event_type = ?", (user_id, event_types,))
            
        conn.commit()
        conn.close()
        
        log_debug(f"History cleared for user {user_id}: removed {event_types} events")
        
    except Exception as e:
        log_error(f"Error clearing history for user {user_id}", e)

