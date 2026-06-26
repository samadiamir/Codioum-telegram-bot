"""
Start and help command handlers.
"""

from keyboards.menus import get_back_menu, get_main_menu, get_help_menu
from utils.conversation_history import add_history_event, get_user_history
from utils.user_state import reset_user_state
from utils.logger import log_error, log_debug, log_warning


def register_start_handlers(bot):
    """
    Register start and help command handlers.

    Args:
        bot: Telebot instance
    """

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """Handle /start command"""
        try:
            reset_user_state(message.from_user.id)
            bot.send_message(
                message.chat.id,
                """\
Welcome to codioum Ai chatbot.
Choose an option below to get started.
""",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} started bot.")
        except Exception as e:
            log_error(f"Error in send_welcome for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Welcome! There was an issue loading the menu. Please try /start again."
                )
            except Exception as send_error:
                log_error("Failed to send welcome message", send_error)

    @bot.message_handler(commands=['reset'])
    def reset_bot(message):
        """Handle /reset command"""
        try:
            reset_user_state(message.from_user.id)
            bot.send_message(
                message.chat.id,
                "The bot has restarted successfully.",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} reset bot state.")
        except Exception as e:
            log_error(f"Error in reset_bot for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Reset failed. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send reset message", send_error)

    @bot.message_handler(commands=['help'])
    def help_bot(message):
        """Handle /help command"""
        try:
            add_history_event(message.from_user.id, "action", "Requested help")
            bot.send_message(
                message.chat.id,
                get_help_menu(),
                reply_markup=get_back_menu()
            )
            log_debug(f"User {message.from_user.id} requested help.")
        except Exception as e:
            log_error(f"Error in help_bot for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error loading help. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send help message", send_error)

    @bot.message_handler(commands=['history'])
    def history_bot(message):
        """Handle /history command"""
        try:
            events = get_user_history(message.from_user.id)
            add_history_event(message.from_user.id, "action", "Viewed history")

            if not events:
                bot.send_message(
                    message.chat.id,
                    "No history available yet. Start chatting or share a location.",
                    reply_markup=get_main_menu()
                )
                log_debug(f"User {message.from_user.id} has no history.")
                return

            formatted = []
            for event in events[-20:]:
                try:
                    timestamp = event.get("timestamp", "unknown time")
                    event_type = event.get("type", "unknown")
                    content = event.get("content", "")
                    if event_type == "location":
                        meta = event.get("metadata", {})
                        formatted.append(
                            f"[{timestamp}] 📍 {content} \nLatitude: {meta.get('latitude')} Longitude: {meta.get('longitude')}"
                        )
                    else:
                        formatted.append(f"[{timestamp}] {event_type}: {content}")
                except Exception as format_error:
                    log_warning(f"Error formatting history event for user {message.from_user.id}", format_error)
                    continue

            bot.send_message(
                message.chat.id,
                "Your recent activity:\n" + "\n\n".join(formatted),
                reply_markup=get_back_menu()
            )
            log_debug(f"History displayed for user {message.from_user.id}.")
        except Exception as e:
            log_error(f"Error in history_bot for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error retrieving your history. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send history message", send_error)

    @bot.message_handler(text=["📜 History"])
    def history_button(message):
        """Handle History button click"""
        try:
            history_bot(message)
        except Exception as e:
            log_error(f"Error in history_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == "⬅️ Back")
    def back_button(message):
        """Handle Back button click"""
        try:
            reset_user_state(message.from_user.id)
            bot.send_message(
                message.chat.id,
                "Returned to the main menu.",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} returned to main menu.")
        except Exception as e:
            log_error(f"Error in back_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Error returning to main menu. Please use /start."
                )
            except Exception as send_error:
                log_error("Failed to send back button message", send_error)
