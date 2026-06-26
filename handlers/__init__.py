"""
Handlers package for registering bot command and message handlers.
"""

from handlers.start import register_start_handlers
from handlers.ai_chat import register_ai_chat_handler
from handlers.weather import register_weather_handler
from handlers.games import register_games_handler


def register_all_handlers(bot):
    """
    Register all bot handlers.

    Args:
        bot: Telebot instance
    """
    register_start_handlers(bot)
    register_weather_handler(bot)
    register_games_handler(bot)
    register_ai_chat_handler(bot)  # Register last as it handles all text
