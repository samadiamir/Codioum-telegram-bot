"""
User session state management.
Tracks per-user interaction mode and stored location.
"""

from datetime import datetime
from utils.logger import log_error, log_debug

user_state = {}


def _ensure_state(user_id):
    """Ensure user state exists in the dictionary."""
    try:
        if not user_id or not isinstance(user_id, int):
            raise ValueError(f"Invalid user_id: {user_id}")

        if user_id not in user_state:
            user_state[user_id] = {
                "mode": "main",
                "location": None,
            }
    except Exception as e:
        log_error(f"Error ensuring state for user {user_id}", e)


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

        _ensure_state(user_id)
        location = {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        user_state[user_id]["location"] = location
        log_debug(f"Location saved for user {user_id}: {latitude}, {longitude}")
        return location
    except Exception as e:
        log_error(f"Error saving location for user {user_id}", e)
        return None


def get_user_location(user_id):
    """Return the user's saved location, or None if missing."""
    try:
        _ensure_state(user_id)
        return user_state[user_id]["location"]
    except Exception as e:
        log_error(f"Error getting location for user {user_id}", e)
        return None


def reset_user_state(user_id):
    """Reset the user state to the default main menu."""
    try:
        user_state[user_id] = {
            "mode": "main",
            "location": None,
        }
        log_debug(f"User state reset for user {user_id}")
    except Exception as e:
        log_error(f"Error resetting state for user {user_id}", e)
