"""
Helper functions for the bot.
"""

from utils.logger import log_error
from utils.constants import Emojis, Messages


def format_message(first_name, content, message_type="general"):
    """
    Format a message with the user's first name and appropriate emoji.

    Args:
        first_name (str|None): User's first name
        content (str): Message content
        message_type (str): Type of message (general, success, error, warning, ai, weather)

    Returns:
        str: Formatted message
    """
    try:
        if not first_name:
            first_name = "Friend"

        if not content or not isinstance(content, str):
            return f"{Messages.ERROR_GENERAL}"

        first_name = str(first_name).strip()[:50]  # Safety limit
        
        # Add appropriate emoji based on message type
        emoji = ""
        if message_type == "success":
            emoji = f"{Emojis.SUCCESS} "
        elif message_type == "error":
            emoji = f"{Emojis.ERROR} "
        elif message_type == "warning":
            emoji = f"{Emojis.WARNING} "
        elif message_type == "ai":
            emoji = f"{Emojis.AI_CHAT} "
        elif message_type == "weather":
            emoji = f"{Emojis.WEATHER} "
        elif message_type == "thinking":
            emoji = f"{Emojis.THINKING} "
        
        return f"{emoji}{content}"
    except Exception as e:
        log_error("Error formatting message", e)
        return f"{Messages.ERROR_GENERAL}"


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


def send_loading_message(bot, chat_id, action="processing"):
    """
    Send a loading message to the user.

    Args:
        bot: Telebot instance
        chat_id: Chat ID to send message to
        action (str): Type of action (processing, thinking, loading)

    Returns:
        int: Message ID of the loading message (for editing later)
    """
    try:
        if action == "thinking":
            text = Messages.THINKING
        elif action == "loading":
            text = Messages.LOADING
        else:
            text = Messages.PROCESSING
        
        message = bot.send_message(chat_id, text)
        return message.message_id
    except Exception as e:
        log_error("Error sending loading message", e)
        return None


def edit_loading_to_success(bot, chat_id, message_id, success_message):
    """
    Edit a loading message to show success.

    Args:
        bot: Telebot instance
        chat_id: Chat ID
        message_id: Message ID to edit
        success_message (str): Success message to show
    """
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{Emojis.SUCCESS} {success_message}"
        )
    except Exception as e:
        log_error("Error editing loading message to success", e)


def edit_loading_to_error(bot, chat_id, message_id, error_message):
    """
    Edit a loading message to show error.

    Args:
        bot: Telebot instance
        chat_id: Chat ID
        message_id: Message ID to edit
        error_message (str): Error message to show
    """
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{Emojis.ERROR} {error_message}"
        )
    except Exception as e:
        log_error("Error editing loading message to error", e)
