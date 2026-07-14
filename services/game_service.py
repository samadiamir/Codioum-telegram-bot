"""
Game service module.
Handles quiz game logic and state.
"""

import requests
from utils.logger import log_debug, log_info, log_error
import threading
import html

game_lock = threading.RLock()  # Reentrant lock - allows same thread to acquire lock multiple times

game_state = {}


def start_game(user_id):
    """Fetch questions and initialize game state."""
    with game_lock:
        try:
            log_info(f"Requesting to the api for user {user_id}")
            response = requests.get("https://opentdb.com/api.php?amount=10&type=boolean&difficulty=easy")
            data = response.json()
    
            if data["response_code"] != 0:
                log_error("API returned error code: " + str(data["response_code"]))
                return False
            question_list = question_list = [
                {
                    **question,  # Keep all fields
                    "question": html.unescape(question["question"])  # Only decode question text
                }
                for question in data["results"]  # Loop through the list
            ]
    
            game_state[user_id] = {
                "questions": question_list,
                "current": 0,
                "score": 0,
            }
            log_info(f"Game started for user {user_id}")
            return True
        except Exception as e:
            log_error(f"Error starting game for user {user_id}", e)
            return False

def get_current_question(user_id):
    """Get the current question for the user."""
    with game_lock:
        try:
            if user_id not in game_state:
                log_error(f"No active game states for user {user_id}.")
            user_data = game_state[user_id]
            question_list = user_data["questions"]
            log_info(f"Getting the current question for user {user_id}")
            current_index = user_data["current"]
            log_info(f"Current index for the user {user_id} --> {current_index}")
            current_question = question_list[current_index]
            return current_question
    
        except Exception as e:
            log_error(f"Error getting questions for user {user_id}", e)
            return None

def has_more_questions(user_id):
    """
    Check if user has more questions to answer.
    Returns True if current question index < total questions.
    """
    with game_lock:
        try:
            log_info(f"Checking for has more questions for user {user_id}")
            user_data = game_state[user_id]
            return user_data["current"] <= len(user_data["questions"])
            
        except Exception as e:
            log_error(f"Error checking more questions for user {user_id}", e)


def next_question(user_id):
    """
    Move to the next question if available.
    Returns True if moved to next question, False if no more questions.
    """
    with game_lock:
        try:
            if has_more_questions(user_id):
                log_debug(f"has more questions : {has_more_questions(user_id)}")
                log_info(f"current index added + 1 for user {user_id}")
                game_state[user_id]["current"] += 1
                return True
            else: 
                return False
        except Exception as e:
            log_error(f"Error moving to next question for user {user_id}", e)


def check_answer(user_id, answer):
    """Check if answer is correct, update score. Does NOT move to next question."""
    with game_lock:
        try:
            
            current_question = get_current_question(user_id)
            correct_answer = current_question["correct_answer"]
            log_debug(f"Checking the answer for user {user_id}")
            if correct_answer.lower() == answer.lower():
                game_state[user_id]["score"] += 1
                return True
            else:
                return False
        except Exception as e:
            log_error(f"Error checking answer for user {user_id}", e)


def get_score(user_id):
    """Get current score."""
    with game_lock:
        try:
            current_score = game_state[user_id]["score"]
            log_debug(f"Getting the current score for user {user_id} ")
            return current_score
        except Exception as e:
            log_error(f"Error for getting score for user {user_id}", e)
            return (0, 10)


def get_results(user_id):
    """Get final results with rank."""
    with game_lock:
        try:
            final_score = get_score(user_id) 
            if final_score <= 3 :
                rank = "Beginner 🥉"
            elif final_score <= 7 :
                rank = "Expert 🥈"
            elif final_score <= 10:
                rank = "Champion 🥇"
            log_debug(f"Getting results for user {user_id}")
    
            return {
                "score": final_score,
                "total": len(game_state[user_id]["questions"]),
                "rank": rank,
            }
    
        except Exception as e:
            log_error(f"Error for getting results for user {user_id}", e)
            return None


def reset_game(user_id):
    """Clear game state for user."""
    with game_lock:
        try:
            log_debug(f"Resseting the game states for user {user_id}")
            del game_state[user_id]
    
        except Exception as e:
            log_error(f"Error for resseting game for user {user_id}", e)