
"""
Games handler module.
Handles game menu and quiz game flow.
"""

from keyboards.menus import get_game_menu, get_main_menu, get_quiz_start_menu, get_answer_menu, get_results_menu
from services.game_service import start_game, get_current_question, check_answer, get_results, reset_game, has_more_questions, next_question, game_state
from utils.conversation_history import add_history_event
from utils.user_state import set_user_mode
from utils.logger import log_error, log_debug, log_info
from telebot import types
from keyboards.menus import get_back_menu
from utils.constants import Emojis, Messages, Buttons

def register_games_handler(bot):
    """
    Register games handler.
    Handles both message text and callback queries.
    """

    # Games button handler (message text)
    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == Buttons.GAMES)
    def games_chat_button(message):
        """Handle Games button click"""
        try:
            user_id = message.from_user.id
            add_history_event(user_id, "action", "Opened games menu")
            bot.send_message(
                chat_id = message.chat.id,
                text=Messages.GAMES_WELCOME,
                reply_markup=get_game_menu()
            )

            log_debug(f"User {user_id} opened games menu.")
        except Exception as e:
            log_error(f"Error in games_chat_button for user {user_id}", e)
            try:
                bot.send_message(message.chat.id, Messages.ERROR_GENERAL)
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    # Callback query handler (inline buttons)
    @bot.callback_query_handler(func=lambda call: call.data in ["game_quiz", "quiz_start", "answer_true", "answer_false", "game_back", "quiz_back", "results_play_again", "results_main_menu"])

        
    def handle_callback(call):
        """Handle all inline button clicks"""
        try:
            bot.answer_callback_query(call.id, "Processing...")
            log_debug("Processing...")

            
            user_id = call.from_user.id
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            log_debug("User_id - Chat_id - message_id --> created in handlers/games")

            try:
                log_debug(f"Game state access test: {game_state.get(user_id, 'NOT_FOUND')}")
            except Exception as e:
                log_error(f"Game state access failed: {e}")

                
            try:
                from utils.user_state import get_user_mode
                mode = get_user_mode(user_id)
                log_debug(f"User mode: {mode}")
            except Exception as e:
                log_error(f"User mode check failed: {e}")

            log_debug(f"Callback data: {call.data}")
            valid_callbacks = ["game_quiz", "quiz_start", "answer_true", "answer_false", "game_back", "quiz_back", "results_play_again", "results_main_menu"]
            if call.data not in valid_callbacks:
                log_error(f"Unknown callback data: {call.data}")
                
            if user_id not in game_state and call.data not in ["game_quiz", "quiz_start", "game_back", "quiz_back", "results_main_menu"]:
                try : 
                    bot.answer_callback_query(
                        call.id,
                        f"{Messages.WARNING_CANCELLED} Your last game has expired. Starting a new game...",
                        show_alert=True
                    )
                    log_debug(f"Trying to start a new game for user {user_id}.")
                    start_game(user_id)
                    question = get_current_question(user_id)
                    current_index = game_state[user_id]["current"]
                    log_info(f"Sending the question to user {user_id}")
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"{Emojis.QUIZ} Question {current_index + 1}:\n\n{question['question']}",
                        reply_markup=get_answer_menu()
                    )
                    
                except Exception as e :
                    log_error(f"Error for starting the new game for user {user_id}. handlers/game 56-75 ", e)
                    bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
                    
                    try:
                        bot.send_message(
                            chat_id = chat_id,
                            text=Messages.ERROR_GENERAL,
                        )
                        
                    except Exception as send_error :
                        log_error(f"Error for sending the recovery message for user {user_id}", send_error)
                        bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
                        
            # Game menu buttons
            elif call.data == "game_quiz":
                from utils.user_state import get_user_mode
                # Check if user is actually in main mode before allowing game start
                if get_user_mode(user_id) != "main":
                    bot.answer_callback_query(call.id, Messages.ERROR_PERMISSION, show_alert=True)
                    return
                
                log_info("Sending welcome message to the quiz game.")
                try: 
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=Messages.QUIZ_WELCOME,
                        reply_markup=get_quiz_start_menu()
                    )
                    log_debug(f"Sending welcome message to the quiz game for user {user_id}")
                except Exception as send_error: 
                    log_error(f"Error for sending the welcome message in quiz game for user {user_id}. handlers/games line 89-98", send_error)
                    bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)

            elif call.data == "game_back":
                from utils.user_state import set_user_mode
                try: 
                    set_user_mode(user_id, "main")
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"{Emojis.HOME} Back to main menu",
                        reply_markup=get_main_menu()
                    )
                    log_debug(f"Trying to get back to the main menu for user {user_id}. user_mode = main")
                except Exception as e :
                    log_error(f"Error for getting the main menu for user {user_id}. handlers/games line 100-112", e)
                    try:
                        bot.send_message(
                            chat_id=chat_id,
                            text=f"{Emojis.HOME} Back to main menu",
                            reply_markup=get_main_menu()
                        )
                    except Exception as send_error:
                        log_error(f"Failed to send main menu to user {user_id}", send_error)
                        bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)


            # Quiz start menu buttons
            elif call.data == "quiz_start":
                from utils.user_state import set_user_mode
                try: 
                    set_user_mode(user_id, "game")
                    start_game(user_id)
                    question = get_current_question(user_id)
                    user_data = game_state[user_id]
                    current_index = user_data["current"]
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"{Emojis.QUIZ} Question {current_index + 1}:\n\n{question['question']}",
                        reply_markup=get_answer_menu()
                    )
                    log_debug(f"Starting the quiz game with showing the first question for user {user_id}")
                except Exception as e :
                    log_error(f"Error showing the question for user {user_id}. handlers/games line 118-132", e)
                    bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
                
            elif call.data == "quiz_back":
                try:
                    from utils.user_state import set_user_mode
                    set_user_mode(user_id, "main")
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"{Emojis.HOME} Back to main menu",
                        reply_markup=get_main_menu()
                    )
                    log_debug(f"Trying to get back to main menu in the quiz by user {user_id}")
                except Exception as e : 
                    log_error(f"Error for getting the main menu for user {user_id}. handlers/games line 100-112", e)
                    try:
                        bot.send_message(
                            chat_id=chat_id,
                            text=f"{Emojis.HOME} Back to main menu",
                            reply_markup=get_main_menu()
                        )
                    except Exception as send_error:
                        log_error(f"Failed to send main menu to user {user_id}", send_error)
                        bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
                    
            # Answer buttons
            elif call.data in ("answer_true", "answer_false"):
                answer = "True" if call.data == "answer_true" else "False"
                correct = check_answer(user_id, answer)
                log_debug("Processing for cheking answers.")
                if correct :
                    text = f"{Emojis.SUCCESS} Correct!"
                else :
                    text = f"{Emojis.ERROR} Wrong!"

                user_data = game_state[user_id]
                
                log_debug("Cheking if there is more questions or not.")
                if user_data["current"] + 1 >= len(user_data["questions"]):
                    # Last question - show results
                    try :
                        results = get_results(user_id)
                        text += f"\n\n{Emojis.STAR} Game Over!\n{Messages.QUIZ_SCORE} {results['score']}/{results['total']}\nRank: {results['rank']}"
                        log_debug("Preparing the text for showing the user the results")
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=text,
                            reply_markup=get_results_menu()
                        )
                        log_debug("Editing message for showing the result.")
                    except Exception as e:
                        log_error(f"Error for showing the result of quiz game for user {user_id}. handlers/games line 179-189", e)
                        bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
                else:
                    # Not last question - show next question
                    try:
                        next_question(user_id)  # Move to next question
                        log_debug("Moving to the next question.")
                        question = get_current_question(user_id)
                        user_data = game_state[user_id]
                        current_index = user_data["current"]
                        text += f"\n\n{Emojis.QUIZ} Question {current_index + 1}:\n\n{question['question']}"
                        log_debug("Editing the message for showing the next question")
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=text,
                            reply_markup=get_answer_menu()
                        )
                    except Exception as e:
                        log_error(f"Error for showing the next question for user {user_id}. handlers/games line 161-177", e)
                        bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)


            # Results menu buttons
            elif call.data == "results_play_again":
                try :
                    from utils.user_state import set_user_mode
                    reset_game(user_id)
                    set_user_mode(user_id, "main")
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f"{Emojis.GAMES} Choose a game:",
                        reply_markup=get_game_menu()
                        
                    )
                except Exception as e :
                    log_error(f"Error playing again for user {user_id}. handlers/game 231-243 ", e)
                    bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)

            elif call.data == "results_main_menu":
                from utils.user_state import set_user_mode
                reset_game(user_id)
                set_user_mode(user_id, "main")
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"{Emojis.HOME} Back to main menu",
                    reply_markup=get_main_menu()
                )

            # Acknowledge the callback (important!)
            bot.answer_callback_query(call.id)

        except Exception as e:
            log_error(f"Error in handle_callback for user {user_id}", e)
            try:
                bot.answer_callback_query(call.id, Messages.ERROR_GENERAL, show_alert=True)
            except Exception as send_error:
                log_error("Failed to send callback error", send_error)