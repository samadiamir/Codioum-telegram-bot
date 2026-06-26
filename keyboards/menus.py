"""
Keyboard menus and inline buttons for the bot.
"""

from telebot import types
from telebot.util import quick_markup

def get_main_menu():
    """
    Get main menu keyboard.

    Returns:
        telebot.types.ReplyKeyboardMarkup: Main menu keyboard
    """
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_ai = types.KeyboardButton("💬 AI Chat")
    btn_weather = types.KeyboardButton("🌤️ Weather")
    btn_games = types.KeyboardButton("🎮 Games")
    btn_history = types.KeyboardButton("📜 History")
    btn_help = types.KeyboardButton("❓ Help")
    markup.add(btn_ai, btn_weather, btn_games, btn_history, btn_help)
    return markup


def get_help_menu():
    """
    Get help menu with contact information.

    Returns:
        str: Help message
    """
    from config.settings import SUPPORT_EMAIL, SUPPORT_ID, SUPPORT_CONTACT

    return f"""\
Do you have any questions?
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
    markup.add(types.KeyboardButton("⬅️ Back"))
    return markup
