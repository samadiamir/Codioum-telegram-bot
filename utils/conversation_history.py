"""
History management module.
Stores and manages per-user event history for AI chat, location sharing,
and other bot actions.
"""

from datetime import datetime
from utils.logger import log_error, log_debug, log_warning

user_history = {}


def _ensure_history(user_id):
    """Ensure user history exists in the dictionary."""
    try:
        if not user_id or not isinstance(user_id, int):
            raise ValueError(f"Invalid user_id: {user_id}")

        if user_id not in user_history:
            user_history[user_id] = []
    except Exception as e:
        log_error(f"Error ensuring history for user {user_id}", e)


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
        _ensure_history(user_id)
        if event_types is None:
            return user_history[user_id]

        if isinstance(event_types, str):
            event_types = [event_types]

        filtered = [event for event in user_history[user_id] if event.get("type") in event_types]
        return filtered
    except Exception as e:
        log_error(f"Error getting history for user {user_id}", e)
        return []


def add_history_event(user_id, event_type, content, metadata=None):
    """
    Add a generic history event for a user.

    Args:
        user_id (int): The user's Telegram ID
        event_type (str): Type of history event, e.g. 'ai_chat', 'location', 'action'
        content (str): Event content or description
        metadata (dict|None): Optional extra data
    """
    try:
        if not event_type or not isinstance(event_type, str):
            raise ValueError(f"Invalid event_type: {event_type}")

        if not content or not isinstance(content, str):
            raise ValueError(f"Invalid content: {content}")

        _ensure_history(user_id)
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": event_type,
            "content": content,
        }
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise ValueError(f"Invalid metadata: {metadata}")
            event["metadata"] = metadata

        user_history[user_id].append(event)
        log_debug(f"History event added for user {user_id}: {event_type}")
        return event
    except Exception as e:
        log_error(f"Error adding history event for user {user_id}", e)
        return None


def add_message_to_history(user_id, role, content):
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

        return add_history_event(user_id, "ai_chat", content, {"role": role})
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
            {
                "latitude": latitude,
                "longitude": longitude,
            }
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
        if user_id not in user_history:
            return

        if event_types is None:
            user_history[user_id] = []
            log_debug(f"All history cleared for user {user_id}")
            return

        if isinstance(event_types, str):
            event_types = [event_types]

        old_count = len(user_history[user_id])
        user_history[user_id] = [
            event for event in user_history[user_id]
            if event.get("type") not in event_types
        ]
        new_count = len(user_history[user_id])
        log_debug(f"History cleared for user {user_id}: removed {old_count - new_count} events")
    except Exception as e:
        log_error(f"Error clearing history for user {user_id}", e)


def get_full_history(user_id):
    """
    Get AI chat history formatted for the AI API request.

    Args:
        user_id (int): The user's Telegram ID

    Returns:
        list: List of role/content message dictionaries
    """
    try:
        ai_events = get_user_history(user_id, event_types="ai_chat")
        history = []
        for event in ai_events:
            try:
                if event.get("metadata") and event["metadata"].get("role"):
                    history.append({
                        "role": event["metadata"]["role"],
                        "content": event.get("content", "")
                    })
            except Exception as event_error:
                log_warning(f"Error processing history event for user {user_id}", event_error)
                continue

        return history
    except Exception as e:
        log_error(f"Error getting full history for user {user_id}", e)
        return []
