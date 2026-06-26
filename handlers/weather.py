"""
Weather command handler.
"""
from services.weather_service import get_weather
from telebot import types
from utils.conversation_history import add_history_event, add_location_to_history
from utils.user_state import set_user_mode, save_user_location, get_user_location, get_user_mode
from keyboards.menus import get_back_menu
from utils.logger import log_error, log_debug, log_warning

def register_weather_handler(bot):
    """
    Register weather command handler.

    Args:
        bot: Telebot instance
    """

    # REGISTER LOCATION HANDLER FIRST - most specific, must be first
    @bot.message_handler(content_types=['location'])
    def weather_location_handler(message):
        """Handle location sharing in weather mode"""
        try:
            log_debug(f"Location message received from user {message.from_user.id}")

            if not message.location:
                log_warning(f"Location message received but location is None for user {message.from_user.id}")
                bot.reply_to(message, "Please share your location to get the weather information.")
                return

            user_mode = get_user_mode(message.from_user.id)
            log_debug(f"User {message.from_user.id} mode: {user_mode}")

            # Only process if in weather mode
            if user_mode != "weather":
                log_debug(f"Location ignored - user {message.from_user.id} not in weather mode (mode={user_mode})")
                return

            latitude = message.location.latitude
            longitude = message.location.longitude

            log_debug(f"Location received from user {message.from_user.id}: {latitude}, {longitude}")

            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                log_warning(f"Invalid location coordinates: {latitude}, {longitude}")
                bot.reply_to(message, "Invalid location coordinates received.")
                return

            save_user_location(message.from_user.id, latitude, longitude)
            log_debug(f"Location saved for user {message.from_user.id}")

            add_location_to_history(
                message.from_user.id,
                latitude,
                longitude,
                description="Location shared for weather lookup"
            )
            log_debug(f"Location added to history for user {message.from_user.id}")

            weather_text = get_weather(latitude=latitude, longitude=longitude)
            log_debug(f"Weather retrieved for user {message.from_user.id}")

            set_user_mode(message.from_user.id, "main")
            bot.reply_to(
                message,
                weather_text,
                reply_markup=get_back_menu()
            )
            log_debug(f"Weather response sent to user {message.from_user.id}")
        except Exception as e:
            log_error(f"Error in weather_location_handler for user {message.from_user.id}", e)
            try:
                bot.reply_to(message, "Error retrieving weather. Please try again.")
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) == "🌤️ Weather" or getattr(message, 'text', None) == "/weather")
    def weather_chat_button(message):
        """Handle Weather button click"""
        try:
            set_user_mode(message.from_user.id, "weather")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton("📍 Share My Location", request_location=True))

            saved_location = get_user_location(message.from_user.id)
            if saved_location:
                markup.add(types.KeyboardButton("Use saved location"))
            markup.add(types.KeyboardButton("⬅️ Back"))

            bot.send_message(
                message.chat.id,
                "🌤️ Weather mode activated! Send me a city name, share your location, or use your saved location.",
                reply_markup=markup
            )
            log_debug(f"User {message.from_user.id} entered weather mode.")
        except Exception as e:
            log_error(f"Error in weather_chat_button for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Sorry, there was an error. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) and get_user_location(message.from_user.id) and get_user_mode(message.from_user.id) == "weather" and getattr(message, 'text', None).strip().lower() == "use saved location")
    def weather_saved_location_handler(message):
        """Handle the saved location weather request"""
        try:
            saved = get_user_location(message.from_user.id)
            if saved:
                weather_text = get_weather(latitude=saved["latitude"], longitude=saved["longitude"])
                set_user_mode(message.from_user.id, "main")
                bot.send_message(
                    message.chat.id,
                    weather_text,
                    reply_markup=get_back_menu()
                )
                log_debug(f"Weather provided for user {message.from_user.id} using saved location.")
            else:
                bot.send_message(
                    message.chat.id,
                    "No saved location found. Please share your location first.",
                    reply_markup=get_back_menu()
                )
        except Exception as e:
            log_error(f"Error in weather_saved_location_handler for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Error retrieving weather. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)

    @bot.message_handler(func=lambda message: getattr(message, 'text', None) and get_user_mode(message.from_user.id) == "weather")
    def weather_city_handler(message):
        """Handle city name weather requests while in weather mode"""
        try:
            city = message.text.strip()
            if not city:
                bot.send_message(
                    message.chat.id,
                    "Please enter a city name or share your location.",
                    reply_markup=get_back_menu()
                )
                return

            log_debug(f"Fetching weather for city: {city} (user {message.from_user.id})")
            weather_text = get_weather(city=city)
            set_user_mode(message.from_user.id, "main")
            bot.send_message(
                message.chat.id,
                weather_text,
                reply_markup=get_back_menu()
            )
        except Exception as e:
            log_error(f"Error in weather_city_handler for user {message.from_user.id}", e)
            try:
                bot.send_message(
                    message.chat.id,
                    "Error retrieving weather. Please try again."
                )
            except Exception as send_error:
                log_error("Failed to send error message", send_error)
