import sys
import time
from pathlib import Path
import telebot
from utils.database import init_db

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.settings import API_TOKEN
from handlers import start, ai_chat, weather, games, sessions
from utils.logger import log_info, log_error, log_warning

if not API_TOKEN:
    log_error("API_KEY environment variable is not set!")
    raise ValueError("API_KEY environment variable is required but not set.")

try:
    bot = telebot.TeleBot(API_TOKEN)
    log_info("Bot initialized successfully.")
except Exception as e:
    log_error("Failed to initialize bot", e)
    raise

init_db()
log_info("Database initialized.")

try:
    # Register handlers
    start.register_start_handlers(bot)
    log_info("Start handlers registered.")

    ai_chat.register_ai_chat_handler(bot)
    log_info("AI chat handlers registered.")

    weather.register_weather_handler(bot)
    log_info("Weather handlers registered.")

    games.register_games_handler(bot)
    log_info("Games handlers registered.")

    sessions.register_session_handlers(bot)
    log_info("Sessions handlers registered.")
except Exception as e:
    log_error("Failed to register handlers", e)
    raise


if __name__ == "__main__":
    while True:
        try:
            log_info("🤖 Bot is starting...")
            bot.send_chat_action(chat_id=bot.get_me().id, action="typing")
            log_info("✅ Bot is running and ready to handle messages.")
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
            break
        except KeyboardInterrupt:
            log_info("Bot stopped by user (KeyboardInterrupt).")
            break
        except Exception as e:
            log_error("Polling error, retrying in 5 seconds", e)
            time.sleep(5)