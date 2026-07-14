"""
Constants for consistent emojis, messages, and UX patterns.
"""

# Consistent Emojis - Same emoji for same action
class Emojis:
    # Navigation
    BACK = "🔙"
    HOME = "🏠"
    MAIN_MENU = "🏠"
    
    # Features
    AI_CHAT = "💬"
    WEATHER = "🌤️"
    GAMES = "🎮"
    HISTORY = "📜"
    HELP = "❓"
    
    # Actions
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    LOADING = "⏳"
    THINKING = "🤔"
    PROCESSING = "⚙️"
    
    # Game
    QUIZ = "🧠"
    TRUE = "✔"
    FALSE = "❌"
    PLAY_AGAIN = "🔄"
    
    # Weather
    LOCATION = "📍"
    SAVE = "💾"
    USE_SAVED = "📍"
    
    # AI Chat
    NEW_CHAT = "🆕"
    SESSIONS = "📋"
    LEARN = "📚"
    COMPACT = "🗜️"
    SAVE_INFO = "💾"
    NEW_CONVERSATION = "🆕 New conversation started."
    
    # Status
    ONLINE = "🟢"
    OFFLINE = "🔴"
    CONNECTED = "🔗"
    
    # Ratings
    STAR = "⭐"
    HEART = "❤️"
    FIRE = "🔥"
    
    # Other
    ROBOT = "🤖"
    USER = "👤"
    TIME = "⏰"
    CALENDAR = "📅"
    BOOK = "📖"
    PENCIL = "✏️"


# Consistent Messages
class Messages:
    # Welcome
    WELCOME = "Welcome! I'm your AI assistant. How can I help you today?"
    WELCOME_BACK = "Welcome back! Ready to continue?"
    
    # Loading
    THINKING = "🤔 Thinking..."
    PROCESSING = "⚙️ Processing your request..."
    LOADING = "⏳ Loading..."
    
    # Success
    SAVED = "✅ Saved successfully!"
    DELETED = "✅ Deleted successfully!"
    UPDATED = "✅ Updated successfully!"
    DONE = "✅ Done!"
    
    # Errors
    ERROR_GENERAL = "❌ Something went wrong. Please try again."
    ERROR_AI = "❌ AI service is temporarily unavailable. Please try again later."
    ERROR_DATABASE = "❌ Database error. Please try again."
    ERROR_INVALID_INPUT = "❌ Invalid input. Please check and try again."
    ERROR_NOT_FOUND = "❌ Not found. Please try again."
    ERROR_PERMISSION = "❌ You don't have permission for this action."
    ERROR_LIMIT = "❌ You've reached the limit. Please try again later."
    
    # Warnings
    WARNING_LONG_MESSAGE = "⚠️ Message is too long. Please shorten it."
    WARNING_EMPTY_MESSAGE = "⚠️ Please send a valid message."
    WARNING_CANCELLED = "⚠️ Action cancelled."
    
    # AI Chat
    AI_MODE_ACTIVATED = "💬 AI Chat mode activated! Send me any question."
    AI_NEW_CONVERSATION = "🆕 New conversation started."
    AI_SESSIONS_LIST = "📋 Your conversation sessions:"
    AI_LEARN_MODE = "📚 Learn mode activated. Tell me something to remember."
    AI_COMPACT_DONE = "🗜️ Conversation compacted. Important info saved."
    AI_SAVED = "💾 Information saved for future reference."
    
    # Weather
    WEATHER_MODE = "🌤️ Weather mode activated! Share your location or enter a city name."
    WEATHER_ERROR = "❌ Could not retrieve weather. Please try again."
    WEATHER_SAVED = "📍 Location saved for future use."
    
    # Games
    GAMES_WELCOME = "🎮 Welcome to games! Choose a game to play."
    QUIZ_WELCOME = "🧠 Welcome to Quiz Game! Ready to challenge your brain?"
    QUIZ_CORRECT = "✅ Correct!"
    QUIZ_WRONG = "❌ Wrong!"
    QUIZ_GAME_OVER = "🏆 Game Over! Here are your results:"
    QUIZ_SCORE = "📊 Your score:"
    
    # Help
    HELP_MESSAGE = """❓ How to use this bot:

💬 AI Chat - Ask me anything
🌤️ Weather - Get weather information
🎮 Games - Play fun games
❓ Help - Show this message

Commands:
/new - Start a fresh conversation
/reset - Reset bot to main menu
/sessions - Shows conversations

Send /start to return to main menu."""
    
    # Commands
    COMMAND_NEW = "🆕 Start a new conversation"
    COMMAND_SESSIONS = "📋 View your sessions"
    COMMAND_LEARN = "📚 Teach me something"
    COMMAND_COMPACT = "Summarize conversation"
    COMMAND_SAVE = "Save important information"


# Button Labels
class Buttons:
    # Main Menu
    AI_CHAT = "💬 AI Chat"
    WEATHER = "🌤️ Weather"
    GAMES = "🎮 Games"
    HISTORY = "📜 History"
    HELP = "❓ Help"
    
    # Navigation
    BACK = "🔙 Back"
    MAIN_MENU = "🏠 Main Menu"
    
    # Weather
    SHARE_LOCATION = "📍 Share My Location"
    USE_SAVED_LOCATION = "📍 Use Saved Location"
    
    # Games
    QUIZ_GAME = "🧠 Quiz Game"
    START = "✔ Start"
    TRUE = "✔ True"
    FALSE = "❌ False"
    PLAY_AGAIN = "🔄 Play Again"
    
    # AI Chat Commands
    NEW_CHAT = "🆕 New Chat"
    SESSIONS = "📋 Sessions"
    LEARN = "📚 Learn"
    COMPACT = "🗜️ Compact"
    SAVE = "💾 Save"