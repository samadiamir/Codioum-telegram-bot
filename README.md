# Codioum AI Telegram Bot 🤖

## 📌 Description

Codioum AI Telegram Bot is a Python-based conversational chatbot built with **pyTelegramBotAPI (telebot)** and powered by large language models through an OpenAI-compatible API (Nara router / OpenModel endpoints).

The bot acts as a lightweight AI assistant inside Telegram, with persistent chat sessions, a quiz game, weather lookups, and a learning-capture mode.

---

## ⚙️ Features

* Telegram integration using `pyTelegramBotAPI`
* AI-powered responses via OpenAI-compatible LLM API (Nara router, `mistral-large`)
* **Chat sessions** — multiple named conversations stored in SQLite per user
* **Learn mode** — capture user preferences to personalize AI responses
* **Quiz game** — True/False trivia game (OpenTDB) with inline keyboards and scoring
* **Weather** — current conditions with humidity, "feels-like", and UV index (Open-Meteo)
* Command handling system (`/start`, `/help`, `/reset`)
* SQLite database for sessions, history, locations, bookmarks
* Centralized UI text/emojis in `utils/constants.py` (Emojis, Messages, Buttons)
* Environment-based configuration using `.env` + `python-dotenv`
* Lightweight polling architecture with retry on AI API failures

---

## 🧠 How It Works

1. User sends a message or taps a menu button in Telegram
2. TeleBot handler routes the message by user mode (chat / weather / games / learn)
3. For AI chat: message is appended to the active session, sent (with history + learned preferences) to the LLM API
4. AI response is returned, stored, and sent back to the chat
5. For games: questions are fetched from OpenTDB and scored inline

---

## 🚀 Installation

### 1. Clone repository

```bash
git clone https://github.com/samadiamir/Codioum-telegram-bot.git
cd Codioum-telegram-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
API_KEY=your_telegram_bot_token
NARA_KEY=your_nara_router_api_key
AI_KEY=your_nara_router_api_key
```

> ⚠️ Never commit your `.env`. It is gitignored.

### 4. Run the bot

```bash
python main.py
```

---

## 📋 Commands

| Command | Description     |
| ------- | --------------- |
| /start  | Start the bot   |
| /help   | Show help info  |
| /reset  | Reset session   |

---

## 🧩 Tech Stack

* Python 3.10+
* pyTelegramBotAPI
* OpenAI-compatible API (Nara router / OpenModel)
* Open-Meteo (weather)
* OpenTDB (quiz questions)
* SQLite (sessions, history, bookmarks)
* python-dotenv

---

## 🔮 Future Features

This project is actively evolving. Planned improvements include:

### 🧠 Memory System
* Persistent chat history per user (✅ implemented via SQLite)
* Context-aware conversations (✅ implemented)

### 🌐 API Upgrades
* Support for multiple AI providers (OpenRouter, Gemini, DeepSeek)
* Dynamic model switching per request

### 💾 Database Integration
* ✅ SQLite for user sessions, history, and bookmarks
* Message logging and analytics

### 🛡️ Stability Improvements
* ✅ Retry mechanism for API failures
* Rate limiting per user
* Error logging system (✅ implemented via `utils/logger.py`)

---

## 📌 Notes

This project is intended for learning and experimentation purposes. It is designed to be a foundation for building more complex AI agents and automation systems inside Telegram.

---

## 👨‍💻 Author

Developed by **Amir Samadi**
