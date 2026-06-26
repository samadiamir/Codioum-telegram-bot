"""
Helper functions for the bot.
"""

from utils.logger import log_error


def format_message(first_name, content):
    """
    Format a message with the user's first name.

    Args:
        first_name (str|None): User's first name
        content (str): Message content

    Returns:
        str: Formatted message
    """
    try:
        if not first_name:
            first_name = "Friend"

        if not content or not isinstance(content, str):
            return "No content to display."

        first_name = str(first_name).strip()[:50]  # Safety limit
        return f"Dear {first_name}\n{content}"
    except Exception as e:
        log_error("Error formatting message", e)
        return content


def is_valid_message(message):
    """
    Validate if a message is valid.

    Args:
        message: Telebot message object

    Returns:
        bool: True if message is valid
    """
    try:
        if not message:
            return False

        text = getattr(message, 'text', None)
        if not text or not isinstance(text, str):
            return False

        return len(text.strip()) > 0
    except Exception as e:
        log_error("Error validating message", e)
        return False
