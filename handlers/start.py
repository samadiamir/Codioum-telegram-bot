"""
Start and help command handlers.
"""

from pydoc import text

from keyboards.menus import get_back_menu, get_main_menu, get_help_menu
from utils.conversation_history import add_history_event, get_user_history, clear_user_history
from utils.user_state import reset_user_state
from utils.logger import log_error, log_debug, log_warning
from utils.constants import Emojis, Messages, Buttons


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
                f"{Emojis.ROBOT} {Messages.WELCOME}",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} started bot.")
        except Exception as e:
            log_error(f"Error in send_welcome for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
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
                f"{Messages.DONE} Bot has been reset successfully.",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} reset bot state.")
        except Exception as e:
            log_error(f"Error in reset_bot for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
                )
            except Exception as send_error:
                log_error("Failed to send reset message", send_error)


    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.BACK)
    def back_button(message):
        """Handle Back button click"""
        try:
            log_debug(f"User {message.from_user.id} pressed the back button")
            reset_user_state(message.from_user.id)
            bot.send_message(
                message.chat.id,
                f"{Emojis.HOME} Returned to the main menu.",
                reply_markup=get_main_menu()
            )
            log_debug(f"User {message.from_user.id} returned to main menu.")
        except Exception as e:
            log_error(f"Error in back_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
                )
            except Exception as send_error:
                log_error("Failed to send back button message", send_error)
    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.HELP)
    def help_button(message):
        """ Handle help button click """
        try:
            add_history_event(message.from_user.id, "action", "Requested help")
            bot.send_message(
                message.chat.id,
                f"{Emojis.HELP} {Messages.HELP_MESSAGE}",
                reply_markup=get_back_menu()
            )
            log_debug(f"User {message.from_user.id} requested help.")
        except Exception as e:
            log_error(f"Error in help_bot for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
                )
            except Exception as send_error:
                log_error("Failed to send help message", send_error)

