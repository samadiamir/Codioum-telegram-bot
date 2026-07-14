"""
AI chat message handler with conversation history.
"""

from telebot import types
from utils.helpers import format_message, send_loading_message, edit_loading_to_success, edit_loading_to_error
from services.ai_service import get_ai_response
from utils.conversation_history import (
    get_user_history,
    add_message_to_history,
    add_history_event,
    clear_user_history,
)
from services.session_service import create_session, rename_session, generate_session_name, get_session_history, get_user_sessions
from utils.user_state import get_user_mode, set_user_mode, get_active_session, set_active_session
from keyboards.menus import get_back_menu, get_main_menu, get_chat_menu
from utils.logger import log_error, log_debug, log_warning
from utils.constants import Emojis, Messages, Buttons
from utils.preferences import add_user_preference
from utils.preferences import format_preferences_for_ai


MAX_LENGTH = 1500

def register_ai_chat_handler(bot):
    """
    Register text message handler for AI chat with history.

    Args:
        bot: Telebot instance
    """

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.AI_CHAT)
    def ai_chat_button(message):
        """Handle AI Chat button click"""
        try:
            set_user_mode(message.from_user.id, "chat")
            bot.send_message(
                message.chat.id,
                Messages.AI_MODE_ACTIVATED,
                reply_markup=get_chat_menu()
            )
            log_debug(f"{Emojis.AI_CHAT} User {message.from_user.id} entered AI chat mode.")
        except Exception as e:
            log_error(f"{Emojis.ERROR} ai_chat_button failed for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
                )
            except Exception as send_error:
                log_error(f"{Emojis.ERROR} Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.NEW_CHAT)
    def new_chat_button(message):
        """Handle New Chat button in chat mode"""
        try:
            user_id = message.from_user.id
            set_active_session(user_id, None)
            bot.send_message(
                message.chat.id,
                f"{Emojis.NEW_CHAT} New conversation started! Send me a message.",
                reply_markup=get_chat_menu()
            )
            log_debug(f"{Emojis.NEW_CHAT} User {user_id} started new conversation via button.")
        except Exception as e:
            log_error(f"{Emojis.ERROR} new_chat_button failed for user {message.from_user.id}", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.SESSIONS)
    def sessions_button(message):
        """Handle Sessions button — show list"""
        try:
            user_id = message.from_user.id
            sessions = get_user_sessions(user_id)

            if not sessions:
                bot.send_message(
                    message.chat.id,
                    f"{Emojis.SESSIONS} No sessions yet. Start chatting!",
                    reply_markup=get_chat_menu()
                )
                return

            markup = types.InlineKeyboardMarkup()
            for session in sessions[:20]:
                btn = types.InlineKeyboardButton(
                    text=f"{Emojis.SESSIONS} {session['name']}",
                    callback_data=f"open_session_{session['id']}"
                )
                markup.add(btn)
            markup.add(types.InlineKeyboardButton(text=Buttons.BACK, callback_data="sessions_back"))

            bot.send_message(
                message.chat.id,
                f"{Emojis.SESSIONS} Your sessions:",
                reply_markup=markup
            )
            log_debug(f"{Emojis.SESSIONS} Sessions list displayed for user {user_id}")
        except Exception as e:
            log_error(f"{Emojis.ERROR} sessions_button failed for user {message.from_user.id}", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)
            
    
    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.LEARN)
    def learn_capture_handler(message):
        try:
            user_id = message.from_user.id
            set_user_mode(user_id, "learn")

            bot.send_message(
                message.chat.id,
                Messages.AI_LEARN_MODE,
                reply_markup=get_chat_menu()
            )
            
        except Exception as e:
            log_error(f"{Emojis.ERROR} learn_capture failed for user {user_id}", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)

    @bot.message_handler(func=lambda message: get_user_mode(message.from_user.id) == "learn" and getattr(message, 'text', None))
    def save_learn(message):
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            
            log_debug(f"Saving preferences for user {user_id}")
            add_user_preference(user_id, message.text)
    
            log_debug(f"{Emojis.LEARN} User preferences saved for user {user_id} ")
            bot.send_message(chat_id, Messages.AI_SAVED, reply_markup=get_chat_menu())
        except Exception as e :
            log_error(f"{Emojis.ERROR} Error for saving user prefrences.", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)


    @bot.message_handler(func=lambda message: getattr(message, 'text', None) not in [Buttons.AI_CHAT, Buttons.WEATHER, Buttons.GAMES, Buttons.HISTORY, Buttons.HELP, Buttons.BACK, "⬅️ Back", Buttons.NEW_CHAT, Buttons.SESSIONS] and getattr(message, 'text', '').strip() and not getattr(message, 'text', '').startswith('/') and get_user_mode(message.from_user.id) != "weather")
    def chat_bot(message):
        """Handle text messages and respond with AI using conversation history"""
        user_message = message.text
        user_id = message.from_user.id

        try:
            if not get_active_session(user_id):
                
                log_debug(f"{Emojis.SESSIONS} Creating session for user {user_id}")
                session_id = create_session(user_id)
                
                set_active_session(user_id, session_id)
                
                log_debug(f"{Emojis.PENCIL} Generating name for session {session_id}")
                session_title = generate_session_name(user_message)

                log_debug(f"{Emojis.SUCCESS} Renamed session {session_id} to '{session_title}'")
                rename_session(session_id, session_title)
            else:
                session_id = get_active_session(user_id)
        except Exception as session_error:
            log_error(f"{Emojis.ERROR} Session creation failed for user {user_id}", session_error)
            bot.send_message(message.chat.id, Messages.ERROR_DATABASE)
            return
            
        try:
            log_debug(f"{Emojis.AI_CHAT} Processing chat for user {user_id}: {user_message[:50]}...")

            if not user_message or not isinstance(user_message, str):
                log_warning(f"{Emojis.WARNING} Invalid message from user {user_id}")
                bot.send_message(
                    message.chat.id,
                    Messages.WARNING_EMPTY_MESSAGE
                )
                return

            #Checking for max lengh
            log_debug(f"{Emojis.WARNING} Checking max length limit")
            if len(user_message) > MAX_LENGTH:
                log_debug(f"{Emojis.WARNING} User {user_id}: Message too long")
                bot.send_message(
                    message.chat.id,
                    Messages.WARNING_LONG_MESSAGE
                )
                return
            
            # Send loading message
            loading_message_id = send_loading_message(bot, message.chat.id, "thinking")
            
            # Get user's conversation history
            try:
                history = get_session_history(session_id)
            except Exception as history_error:
                log_error(f"{Emojis.ERROR} History retrieval failed for user {user_id}", history_error)
                history = []

            #Formatting the user prefrences for sending to ai
            prefs = format_preferences_for_ai(user_id)
            
            # Get AI response with history context
            ai_response = get_ai_response(user_message, history, system_context=prefs)

            if ai_response:
                try:
                    # Add user message and AI response to history
                    add_message_to_history(user_id, "user", user_message, session_id=session_id)
                    add_message_to_history(user_id, "assistant", ai_response, session_id=session_id)
                    add_history_event(user_id, "action", "AI chat exchange")
                except Exception as store_error:
                    log_error(f"{Emojis.ERROR} Failed to store chat history for user {user_id}", store_error)

                # Format and send response
                try:
                    formatted_message = format_message(
                        message.chat.first_name or "Friend",
                        ai_response,
                        "ai"
                    )
                    
                    # Edit loading message to show success
                    if loading_message_id:
                        edit_loading_to_success(bot, message.chat.id, loading_message_id, "Response ready!")
                    
                    bot.send_message(
                        message.chat.id,
                        formatted_message,
                        reply_markup=get_back_menu()
                    )
                    log_debug(f"{Emojis.SUCCESS} AI response sent to user {user_id}")
                except Exception as send_error:
                    log_error(f"{Emojis.ERROR} Failed to send formatted message to user {user_id}", send_error)
                    bot.send_message(
                        message.chat.id,
                        ai_response,
                        reply_markup=get_back_menu()
                    )
            else:
                if loading_message_id:
                    edit_loading_to_error(bot, message.chat.id, loading_message_id, Messages.ERROR_AI)
                else:
                    bot.send_message(
                        message.chat.id,
                        Messages.ERROR_AI
                    )

        except Exception as e:
            log_error(f"{Emojis.ERROR} chat_bot failed for user {user_id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    Messages.ERROR_GENERAL
                )
            except Exception as error_send:
                log_error(f"{Emojis.ERROR} Failed to send error message to user {user_id}", error_send)
