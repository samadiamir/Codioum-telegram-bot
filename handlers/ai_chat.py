"""
AI chat message handler with conversation history.
"""

from utils.helpers import format_message
from services.ai_service import get_ai_response
from utils.conversation_history import (
    get_user_history,
    add_message_to_history,
    add_history_event,
    clear_user_history,
    get_full_history
)
from utils.user_state import get_user_mode, set_user_mode
from keyboards.menus import get_back_menu, get_main_menu
from utils.logger import log_error, log_debug, log_warning


def register_ai_chat_handler(bot):
    """
    Register text message handler for AI chat with history.

    Args:
        bot: Telebot instance
    """

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == "💬 AI Chat")
    def ai_chat_button(message):
        """Handle AI Chat button click"""
        try:
            set_user_mode(message.from_user.id, "chat")
            bot.send_message(
                message.chat.id,
                "💬 AI Chat mode activated! Send me any question and I'll help you.",
                reply_markup=get_back_menu()
            )
            log_debug(f"User {message.from_user.id} entered AI chat mode.")
        except Exception as e:
            log_error(f"Error in ai_chat_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) not in ["💬 AI Chat", "🌤️ Weather", "🎮 Games", "📜 History", "❓ Help", "⬅️ Back"] and getattr(message, 'text', '').strip() and not getattr(message, 'text', '').startswith('/') and get_user_mode(message.from_user.id) != "weather")
    def chat_bot(message):
        """Handle text messages and respond with AI using conversation history"""
        user_message = message.text
        user_id = message.from_user.id

        try:
            log_debug(f"Processing chat for user {user_id}: {user_message[:50]}...")

            if not user_message or not isinstance(user_message, str):
                log_warning(f"Invalid message from user {user_id}")
                bot.send_message(
                    message.chat.id,
                    "Please send a valid text message."
                )
                return

            # Get user's conversation history
            try:
                history = get_full_history(user_id)
            except Exception as history_error:
                log_error(f"Error retrieving history for user {user_id}", history_error)
                history = []

            # Get AI response with history context
            ai_response = get_ai_response(user_message, history)

            if ai_response:
                try:
                    # Add user message and AI response to history
                    add_message_to_history(user_id, "user", user_message)
                    add_message_to_history(user_id, "assistant", ai_response)
                    add_history_event(user_id, "action", "AI chat exchange")
                except Exception as store_error:
                    log_error(f"Error storing chat history for user {user_id}", store_error)

                # Format and send response
                try:
                    formatted_message = format_message(
                        message.chat.first_name or "Friend",
                        ai_response
                    )
                    bot.send_message(
                        message.chat.id,
                        formatted_message,
                        reply_markup=get_back_menu()
                    )
                    log_debug(f"AI response sent to user {user_id}")
                except Exception as send_error:
                    log_error(f"Error sending formatted message to user {user_id}", send_error)
                    bot.send_message(
                        message.chat.id,
                        ai_response,
                        reply_markup=get_back_menu()
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was a problem with the AI API ⚠. Please try again."
                )

        except Exception as e:
            log_error(f"Error in chat_bot for user {user_id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "An unexpected error occurred. Please try again later."
                )
            except Exception as error_send:
                log_error(f"Failed to send error message to user {user_id}", error_send)
