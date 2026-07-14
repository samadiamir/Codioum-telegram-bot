"""
Session management handlers.
Handles New Chat, Sessions list, and session selection.
"""

from keyboards.menus import get_main_menu, get_back_menu, get_chat_menu
from services.session_service import create_session, get_session_history, get_user_sessions
from utils.user_state import set_user_mode, set_active_session
from utils.logger import log_error, log_debug
from utils.constants import Emojis, Messages, Buttons
from telebot import types


def register_session_handlers(bot):
    """Register session management handlers."""
    @bot.message_handler(commands=['new'])
    def new_chat_command(message):
        try:
            user_id = message.from_user.id
            
            set_user_mode(user_id, "chat")
            set_active_session(user_id, None)

            bot.send_message(
                message.chat.id,
                f"{Emojis.NEW_CHAT} New conversation started! Send me a message.",
                reply_markup=get_back_menu()
            )
            log_debug(f"{Emojis.NEW_CHAT} User {user_id} started new conversation.")
        except Exception as e:
            log_error(f"{Emojis.ERROR} /new command failed for user {message.from_user.id}", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.SESSIONS)
    def sessions_list_handler(message):
        try:
            user_id = message.from_user.id

            result = get_user_sessions(user_id)
            if not result:
                bot.send_message(message.chat.id, f"{Emojis.SESSIONS} No sessions yet. Start chatting!")

            markup = types.InlineKeyboardMarkup()
            for session in result:
                button = types.InlineKeyboardButton(text=f"{Emojis.SESSIONS} {session['name']}", callback_data = f"open_session_{session['id']}")
                markup.add(button)
            back_button = types.InlineKeyboardButton(text=Buttons.BACK, callback_data="sessions_back")
            markup.add(back_button)

            bot.send_message(
                message.chat.id,
                f"{Emojis.SESSIONS} Your sessions:",
                reply_markup=markup
            )


            log_debug(f"{Emojis.SESSIONS} Sessions list displayed for user {user_id}")
        except Exception as e:
            log_error(f"{Emojis.ERROR} Sessions list failed for user {message.from_user.id}", e)
            bot.send_message(message.chat.id, Messages.ERROR_GENERAL)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("open_session_"))
    def open_session_callback(call):
        try:
            user_id = call.from_user.id
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            session_id = int(call.data.replace("open_session_", ""))
            set_active_session(user_id, session_id)
            
            # Load history and build preview
            history = get_session_history(session_id)
            
            if history:
                # Show last 3 messages as preview
                preview = ""
                for msg in history[-3:]:
                    role = "You" if msg["role"] == "user" else "Bot"
                    preview += f"\n💬 {role}: {msg['content'][:80]}..."
                
                bot.answer_callback_query(call.id, f"{Emojis.SUCCESS} Session loaded!")
                bot.send_message(
                    chat_id,
                    f"{Emojis.SESSIONS} Session loaded!{preview}",
                    reply_markup=get_chat_menu()
                )
            else:
                bot.answer_callback_query(call.id, f"{Emojis.SUCCESS} Session loaded!")
                bot.send_message(
                    chat_id,
                    f"{Emojis.SESSIONS} Session loaded! Send a message to continue.",
                    reply_markup=get_chat_menu()
                )
            
            log_debug(f"{Emojis.SESSIONS} User {user_id} opened session {session_id}")
        except Exception as e:
            log_error(f"{Emojis.ERROR} Open session failed for user {call.from_user.id}", e)
            bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)


    @bot.callback_query_handler(func=lambda call: call.data == "sessions_back")
    def sessions_back_callback(call):
        try:
            user_id = call.from_user.id
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            set_user_mode(user_id, "main")

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"{Emojis.HOME} Back to main menu",
                reply_markup=get_main_menu()
            )

        except Exception as e:
            log_error(f"{Emojis.ERROR} Sessions back failed for user {call.from_user.id}", e)
            bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
