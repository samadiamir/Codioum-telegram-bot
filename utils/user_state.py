"""
User session state management.
Tracks per-user interaction mode and stored location.
"""

from datetime import datetime
from utils.logger import log_error, log_debug
from utils.database import get_connection

user_state = {}


def _ensure_state(user_id):
    """Ensure user state exists in the dictionary."""
    try:
        if not user_id or not isinstance(user_id, int):
            raise ValueError(f"Invalid user_id: {user_id}")

        if user_id not in user_state:
            user_state[user_id] = {
                "mode": "main",
                "session_id": None
            }
    except Exception as e:
        log_error(f"Error ensuring state for user {user_id}", e)

# Setting and getting session_id

def set_active_session(user_id: int, session_id) -> None:
    """Set the current session for a user."""
    
    try:
        if not session_id or not isinstance(session_id, int):
            raise ValueError(f"Invalid session_id: {session_id}")
        
        _ensure_state(user_id)
        user_state[user_id]["session_id"] = session_id
        log_debug(f"User {user_id} session_id set to: {session_id}")
    except Exception as e:
        log_error(f"Error setting session_id for user {user_id}", e)


def get_active_session(user_id: int) -> int:
    """Get the current session_id for a user."""

    try:
        _ensure_state(user_id)
        session_id = user_state[user_id]["session_id"]
        return session_id
    except Exception as e:
        log_error(f"Error getting session_id for user {user_id}", e)
        return None
    

# Setting and getting mode
def set_user_mode(user_id, mode):
    """Set the current interaction mode for a user."""
    try:
        if not mode or not isinstance(mode, str):
            raise ValueError(f"Invalid mode: {mode}")

        _ensure_state(user_id)
        user_state[user_id]["mode"] = mode
        log_debug(f"User {user_id} mode set to: {mode}")
    except Exception as e:
        log_error(f"Error setting mode for user {user_id}", e)


def get_user_mode(user_id):
    """Get the current interaction mode for a user."""
    try:
        _ensure_state(user_id)
        mode = user_state[user_id]["mode"]
        return mode or "main"
    except Exception as e:
        log_error(f"Error getting mode for user {user_id}", e)
        return "main"


def save_user_location(user_id, latitude, longitude):
    """Save a user's last known location."""
    try:
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError(f"Invalid coordinates: {latitude}, {longitude}")

        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError(f"Coordinates out of range: {latitude}, {longitude}")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_locations (user_id, latitude, longitude, saved_at)
            VALUES(?, ?, ?, ?)

        """, (user_id, latitude, longitude, datetime.utcnow().isoformat() + "Z"))
        conn.commit()
        conn.close()

        log_debug(f"Location saved for user {user_id}: {latitude}, {longitude}")
        return {"latitude": latitude, "longitude": longitude}
    except Exception as e:
        log_error(f"Error saving location for user {user_id}", e)
        return None

def get_user_location(user_id):
    """Return the user's saved location, or None if missing."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM user_locations WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        conn.close()
        
        if row:
            return {"latitude": row["latitude"], "longitude": row["longitude"]}
            
        return None
        
    except Exception as e:
        log_error(f"Error getting location for user {user_id}", e)
        return None

def reset_user_state(user_id):
    """Reset the user state to the default main menu."""
    try:
        user_state[user_id] = {
            "mode": "main",
            "session_id": None
        }
        
        log_debug(f"User state reset for user {user_id}")
    except Exception as e:
        log_error(f"Error resetting state for user {user_id}", e)
