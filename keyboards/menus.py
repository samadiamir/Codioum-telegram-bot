"""
Keyboard menus and inline buttons for the bot.
"""

from telebot import types
from telebot.util import quick_markup
from utils.constants import Emojis, Messages, Buttons


def get_main_menu():
    """
    Get main menu keyboard.
    Returns:
        telebot.types.ReplyKeyboardMarkup: Main menu keyboard
    """
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_ai = types.KeyboardButton(Buttons.AI_CHAT)
    btn_weather = types.KeyboardButton(Buttons.WEATHER)
    btn_games = types.KeyboardButton(Buttons.GAMES)
    btn_help = types.KeyboardButton(Buttons.HELP)
    markup.add(btn_ai, btn_weather, btn_games, btn_help)
    return markup


def get_chat_menu():
    """
    Get keyboard for AI chat mode — New Chat, Sessions, Back, Learn.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_new = types.KeyboardButton(Buttons.NEW_CHAT)
    btn_sessions = types.KeyboardButton(Buttons.SESSIONS)
    btn_learn = types.KeyboardButton(Buttons.LEARN)
    btn_back = types.KeyboardButton(Buttons.BACK)
    markup.add(btn_new, btn_sessions, btn_back, btn_learn)
    return markup


def get_help_menu():
    """
    Get help menu with contact information.

    Returns:
        str: Help message
    """
    from config.settings import SUPPORT_EMAIL, SUPPORT_ID, SUPPORT_CONTACT

    return f"""\
{Messages.HELP_MESSAGE}
Contact us:
Email: {SUPPORT_EMAIL}
ID: {SUPPORT_ID}
Support: {SUPPORT_CONTACT}
"""


def get_back_menu():
    """
    Get a back button keyboard to return to the main menu.

    Returns:
        telebot.types.ReplyKeyboardMarkup: Back button keyboard
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(Buttons.BACK))
    return markup

# Game inline keyboards
def get_game_menu():
    """ Get inline keyboard for game selection. """
    markup = types.InlineKeyboardMarkup()
    btn_quiz = types.InlineKeyboardButton(text=Buttons.QUIZ_GAME, callback_data="game_quiz")
    btn_back = types.InlineKeyboardButton(text=Buttons.BACK, callback_data="game_back")
    markup.add(btn_quiz, btn_back)
    return markup

def get_quiz_start_menu(): 
    """ Get inline keyboards for the game. """
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton(text=Buttons.START, callback_data="quiz_start")
    btn_back = types.InlineKeyboardButton(text=Buttons.BACK, callback_data="quiz_back")
    markup.add(btn_back, btn_start)
    return markup

def get_answer_menu():
    """ Get inline keyboards for 'True' and 'False' buttons. """
    markup = types.InlineKeyboardMarkup()
    btn_true = types.InlineKeyboardButton(text=Buttons.TRUE, callback_data = "answer_true")
    btn_false= types.InlineKeyboardButton(text=Buttons.FALSE, callback_data="answer_false")
    markup.add(btn_false, btn_true)
    return markup

def get_results_menu() :
    """ Get inline keyboards for the end of the game and showing the 'Play again', 'Main menu' button """
    markup = types.InlineKeyboardMarkup()
    btn_again = types.InlineKeyboardButton(text=Buttons.PLAY_AGAIN, callback_data="results_play_again")
    btn_home = types.InlineKeyboardButton(text=Buttons.MAIN_MENU, callback_data="results_main_menu")
    markup.add(btn_again, btn_home)
    return markup

# Use saved location in weather mode
def use_saved_loc() :
    """ Get inline keyboards for using the last location saved or save a new location """
    markup = types.InlineKeyboardMarkup()
    btn_save = types.InlineKeyboardButton(text=Buttons.USE_SAVED_LOCATION, callback_data="weather_saved_location")
    btn_new = types.InlineKeyboardButton(text=Buttons.MAIN_MENU, callback_data="weather_new_location")
    markup.add(btn_new, btn_save)
    return markup
