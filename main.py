import telebot
from dotenv import load_dotenv
import os
from openai import OpenAI
from telebot import types

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
AI_KEY = os.environ.get("AI_KEY")
GAP_API = os.environ.get("GAP_API")

client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=GAP_API)

bot = telebot.TeleBot(API_TOKEN)

#Handling the /start and /help command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Welcome to codioum Ai chatbot.
Start with: Hello, explain python.
"""
)

@bot.message_handler(commands=['reset'])
def reset_bot(message):
    bot.send_message(
message.chat.id,
"The bot has restarted succesfully."
)

@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.reply_to(message, """\
Do you have any questions?
Contact us:
Email: Samadi.amirmohammad97@gmail.com
Id: @GraceA_Ls
Support: @CortexShadow
""")

@bot.message_handler(content_types=['text'])
def chat_bot(message):
    user_message = message.text
    print(f"User: {user_message}")
    response = client.chat.completions.create(
        model="qwen3-235b-a22b",
        messages=[
            {"role": "user", "content": user_message}
        ]
)
    print(f"Bot: {response.choices[0].message.content}")
    bot.send_message(message.chat.id, f"Dear {message.chat.username}\n{response.choices[0].message.content}")

bot.infinity_polling()
