# Codioum AI Telegram Bot 🤖

## 📌 Description

Codioum AI Telegram Bot is a Python-based conversational chatbot built with **pyTelegramBotAPI (telebot)** and powered by large language models through an external API (OpenModel / OpenAI-compatible endpoints).

The bot acts as a lightweight AI assistant inside Telegram, capable of answering user questions in natural language and serving as a foundation for more advanced AI-driven automation tools.

---

## ⚙️ Features

* Telegram integration using `pyTelegramBotAPI`
* AI-powered responses using external LLM APIs
* Command handling system (`/start`, `/help`, `/reset`)
* Environment-based configuration using `.env`
* Lightweight and fast polling architecture
* Simple and extendable code structure

---

## 🧠 How It Works

1. User sends a message in Telegram
2. Message is captured via TeleBot handler
3. Text is sent to an LLM API (e.g., Qwen / DeepSeek)
4. AI response is returned
5. Bot sends the response back to Telegram chat

---

## 🚀 Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/codioum-ai-bot.git
cd codioum-ai-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
API_KEY=your_telegram_bot_token
AI_KEY=your_ai_api_key
GAP_API=your_model_api_key
```

### 4. Run the bot

```bash
python main.py
```

---

## 🧾 Commands

| Command | Description    |
| ------- | -------------- |
| /start  | Start the bot  |
| /help   | Show help info |
| /reset  | Reset session  |

---

## 🧩 Tech Stack

* Python 3.10+
* pyTelegramBotAPI
* OpenAI-compatible API (OpenModel / OpenRouter / GapGPT)
* dotenv

---

## 🔮 Future Features

This project is actively evolving. Planned improvements include:

### 🧠 Memory System

* Persistent chat history per user
* Context-aware conversations (ChatGPT-like behavior)

### 🌐 API Upgrades

* Support for multiple AI providers (OpenRouter, Gemini, DeepSeek)
* Dynamic model switching per request

### 💾 Database Integration

* SQLite / PostgreSQL for user sessions
* Message logging and analytics

### 🧑‍💻 Advanced Commands

* `/image` → AI image generation
* `/voice` → speech-to-text input
* `/summary` → summarize long texts

### 🛡️ Stability Improvements

* Retry mechanism for API failures
* Rate limiting per user
* Error logging system

---

## 📌 Notes

This project is intended for learning and experimentation purposes. It is designed to be a foundation for building more complex AI agents and automation systems inside Telegram.

---

## 👨‍💻 Author

Developed by **Amir**

---
