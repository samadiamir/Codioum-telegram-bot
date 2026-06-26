"""
Games handler module.
"""

from keyboards.menus import get_back_menu
from utils.conversation_history import add_history_event
from utils.logger import log_error, log_debug


def register_games_handler(bot):
    """
    Register games handler.

    Args:
        bot: Telebot instance
    """
    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == "🎮 Games")
    def games_chat_button(message):
        """Handle Games button click"""
        try:
            add_history_event(message.from_user.id, "action", "Opened games menu")
            bot.send_message(
                message.chat.id,
                "🎮 Games mode activated! This feature is not yet implemented.",
                reply_markup=get_back_menu()
            )
            log_debug(f"User {message.from_user.id} opened games menu.")
        except Exception as e:
            log_error(f"Error in games_chat_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(commands=['games'])
    def games_command(message):
        """Handle /games command"""
        try:
            add_history_event(message.from_user.id, "action", "Used /games command")
            bot.reply_to(message, "Games feature is not yet implemented.")
            log_debug(f"User {message.from_user.id} used /games command.")
        except Exception as e:
            log_error(f"Error in games_command for user {message.from_user.id}", e)
            try:
                bot.reply_to(message, "Sorry, there was an error. Please try again.")
            except Exception as send_error:
                log_error("Failed to send error message", send_error)
