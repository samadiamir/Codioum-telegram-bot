"""
Weather service module using Open-Meteo.
Supports city name lookup via Open-Meteo geocoding and saved coordinates.
"""

import requests
from utils.logger import log_error, log_warning, log_debug

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_DESCRIPTION = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear",
    2: "⛅ Partly cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Fog",
    48: "🌫️ Depositing rime fog",
    51: "🌧️ Drizzle: Light",
    53: "🌧️ Drizzle: Moderate",
    55: "🌧️ Drizzle: Dense",
    56: "🌧️ Freezing Drizzle: Light",
    57: "🌧️ Freezing Drizzle: Dense",
    61: "🌧️ Rain: Slight",
    63: "🌧️ Rain: Moderate",
    65: "🌧️ Rain: Heavy",
    66: "🌧️ Freezing Rain: Light",
    67: "🌧️ Freezing Rain: Heavy",
    71: "🌨️ Snow fall: Slight",
    73: "🌨️ Snow fall: Moderate",
    75: "🌨️ Snow fall: Heavy",
    77: "🌨️ Snow grains",
    80: "🌧️ Rain showers: Slight",
    81: "🌧️ Rain showers: Moderate",
    82: "🌧️ Rain showers: Violent",
    85: "🌨️ Snow showers: Slight",
    86: "🌨️ Snow showers: Heavy",
    95: "⛈️ Thunderstorm: Slight",
    96: "⛈️ Thunderstorm with slight hail",
    99: "⛈️ Thunderstorm with heavy hail",
}

TEMPERATURE_FEELING = {
    "🥶 Freezing": (-50, -10),
    "❄️ Cold": (-9, 5),
    "😊 Cool": (6, 15),
    "🌤️ Warm": (16, 25),
    "🔥 Hot": (26, 40),
    "🆘 Extreme heat": (41, 60),
}


def _get_temperature_feeling(temp):
    """Convert temperature to a human-friendly feeling."""
    for feeling, (low, high) in TEMPERATURE_FEELING.items():
        if low <= temp <= high:
            return feeling
    return "🌡️ Unknown"


def _get_uv_level(uv):
    """Convert UV index to a human-readable level."""
    try:
        uv = float(uv)
        if uv < 3:
            return "Low"
        elif uv < 6:
            return "Moderate"
        elif uv < 8:
            return "High"
        elif uv < 11:
            return "Very High"
        else:
            return "Extreme"
    except (ValueError, TypeError):
        return "Unknown"

def _format_weather(data, location_name=None):
    """Format weather data into a readable string."""
    try:
        if not data:
            return "Weather data is unavailable."

        current = data.get("current_weather", {})
        if not current:
            return "Weather data is unavailable."
        code = current.get("weathercode")
        temperature = current.get("temperature")
        weather = WEATHER_DESCRIPTION.get(code, "Unknown")
        time = current.get("time", "")
        time = time.split("T")[1] if "T" in time else time

        # Get additional data from hourly (first hour = current)
        hourly_data = data.get("hourly", {})

        humidity_data = hourly_data.get("relativehumidity_2m")
        humidity = humidity_data[0] if humidity_data else "N/A"

        feels_like_data = hourly_data.get("apparent_temperature")
        feels_like = feels_like_data[0] if feels_like_data else "N/A"

        uv_index_data = hourly_data.get("uv_index")
        uv_index = uv_index_data[0] if uv_index_data else "N/A"

        # UV level description
        uv_level = _get_uv_level(uv_index)

        location = location_name or f"{data.get('latitude')},{data.get('longitude')}"
        feeling = _get_temperature_feeling(temperature)
        return (
            f"📍 {location}\n\n"
            f"{weather}\n\n"
            f"🌡️ Temperature: {temperature}°C ({feeling})\n"
            f"🤔 Feels like: {feels_like}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"☀️ UV Index: {uv_index} ({uv_level})\n"
            f"🕐 Updated: {time}"
        )
    except Exception as e:
        log_error("Error formatting weather data", e)
        return "Error processing weather data."


def _geocode_city(city):
    """Geocode a city name to coordinates."""
    try:
        if not city or not isinstance(city, str):
            log_warning(f"Invalid city name: {city}")
            return None

        city = city.strip()
        if not city:
            return None

        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        log_debug(f"Geocoding city: {city}")
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("results")

        if not results:
            log_warning(f"No geocoding results for city: {city}")
            return None

        log_debug(f"Geocoding successful for {city}")
        return results[0]

    except requests.exceptions.Timeout:
        log_error(f"Geocoding timeout for city: {city}")
        return None
    except requests.exceptions.ConnectionError as e:
        log_error(f"Connection error during geocoding", e)
        return None
    except requests.exceptions.RequestException as e:
        log_error(f"Geocoding request failed for city: {city}", e)
        return None
    except Exception as e:
        log_error(f"Unexpected error during geocoding", e)
        return None


def get_weather(city=None, latitude=None, longitude=None):
    """
    Get weather information for a city or coordinates.

    Args:
        city (str|None): City name
        latitude (float|None): Latitude
        longitude (float|None): Longitude

    Returns:
        str: Weather information or error message
    """
    try:
        location_name = None

        if city:
            log_debug(f"Processing weather request for city: {city}")
            geocode = _geocode_city(city)
            if not geocode:
                return f"Could not find coordinates for city '{city}'."
            latitude = geocode.get("latitude")
            longitude = geocode.get("longitude")
            location_name = geocode.get("name")
            if geocode.get("country"):
                location_name += f", {geocode.get('country')}"

        if latitude is None or longitude is None:
            log_warning("No location provided for weather lookup.")
            return "No location or city provided for weather lookup."

        # Validate coordinates
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError) as e:
            log_error("Invalid coordinates provided", e)
            return "Invalid coordinates provided."

        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            log_warning(f"Coordinates out of range: {latitude}, {longitude}")
            return "Coordinates out of valid range."

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            "hourly": "relativehumidity_2m,apparent_temperature,uv_index",
            "temperature_unit": "celsius",
            "windspeed_unit": "kmh",
            "precipitation_unit": "mm",
        }

        log_debug(f"Fetching weather for coordinates: {latitude}, {longitude}")
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()

        weather_data = response.json()
        log_debug("Weather data retrieved successfully.")
        return _format_weather(weather_data, location_name=location_name)

    except requests.exceptions.Timeout:
        log_error("Weather API request timeout")
        return "Weather service is currently unavailable. Please try again later."
    except requests.exceptions.ConnectionError as e:
        log_error("Connection error to weather API", e)
        return "Cannot connect to weather service. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        log_error("HTTP error from weather API", e)
        return "Weather service returned an error. Please try again."
    except requests.exceptions.RequestException as e:
        log_error("Weather API request error", e)
        return "Weather API error. Please try again later."
    except ValueError as e:
        log_error("Weather API returned invalid data", e)
        return "Weather API returned invalid data."
    except Exception as e:
        log_error("Unexpected error in weather service", e)
        return "An unexpected error occurred. Please try again later."
