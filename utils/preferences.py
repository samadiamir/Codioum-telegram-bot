"""
User preferences manager.
Stores learned preferences in JSON file.
"""

import json
import os
from datetime import datetime
from utils.logger import log_error, log_debug, log_info

# Path to preferences file
PREFERENCES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_preferences.json")


def load_preferences():
    """
    Load preferences from JSON file.
    
    Returns:
        dict: All user preferences
    """
    try:
        if not os.path.exists(PREFERENCES_PATH):
            return {}
        
        with open(PREFERENCES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_error("Failed to load preferences", e)
        return {}


def save_preferences(preferences):
    """
    Save preferences to JSON file.
    
    Args:
        preferences (dict): All user preferences to save
    """
    try:
        with open(PREFERENCES_PATH, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, ensure_ascii=False)
        log_info("Preferences saved successfully.")
    except Exception as e:
        log_error("Failed to save preferences", e)


def get_user_preferences(user_id):
    """
    Get preferences for a specific user.
    
    Args:
        user_id (int): Telegram user ID
        
    Returns:
        list: List of preference strings
    """
    try:
        preferences = load_preferences()
        user_id_str = str(user_id)
        
        if user_id_str in preferences:
            return preferences[user_id_str].get("preferences", [])
        return []
    except Exception as e:
        log_error(f"Failed to get preferences for user {user_id}", e)
        return []


def add_user_preference(user_id, preference):
    """
    Add a preference for a user.
    
    Args:
        user_id (int): Telegram user ID
        preference (str): Preference to add
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        preferences = load_preferences()
        user_id_str = str(user_id)
        
        if user_id_str not in preferences:
            preferences[user_id_str] = {
                "preferences": [],
                "created_at": datetime.now().isoformat()
            }
        
        # Add preference if not already exists
        if preference not in preferences[user_id_str]["preferences"]:
            preferences[user_id_str]["preferences"].append(preference)
            preferences[user_id_str]["updated_at"] = datetime.now().isoformat()
            save_preferences(preferences)
            log_info(f"Added preference for user {user_id}: {preference}")
            return True
        else:
            log_debug(f"Preference already exists for user {user_id}: {preference}")
            return False
    except Exception as e:
        log_error(f"Failed to add preference for user {user_id}", e)
        return False


def remove_user_preference(user_id, preference):
    """
    Remove a preference for a user.
    
    Args:
        user_id (int): Telegram user ID
        preference (str): Preference to remove
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        preferences = load_preferences()
        user_id_str = str(user_id)
        
        if user_id_str in preferences:
            if preference in preferences[user_id_str]["preferences"]:
                preferences[user_id_str]["preferences"].remove(preference)
                preferences[user_id_str]["updated_at"] = datetime.now().isoformat()
                save_preferences(preferences)
                log_info(f"Removed preference for user {user_id}: {preference}")
                return True
        return False
    except Exception as e:
        log_error(f"Failed to remove preference for user {user_id}", e)
        return False


def format_preferences_for_ai(user_id):
    """
    Format user preferences for AI context.
    
    Args:
        user_id (int): Telegram user ID
        
    Returns:
        str: Formatted preferences string for AI
    """
    try:
        preferences = get_user_preferences(user_id)
        
        if not preferences:
            return ""
        
        prefs_text = "\n".join(f"- {pref}" for pref in preferences)
        return f"\n\nUser Preferences:\n{prefs_text}\nPlease respect these preferences in your responses."
    except Exception as e:
        log_error(f"Failed to format preferences for user {user_id}", e)
        return ""