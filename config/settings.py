import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
API_TOKEN = os.environ.get("API_KEY")

# API for create questions
TRIVIA_URL = "https://opentdb.com/api.php?amount=10&type=boolean"

# AI Configuration
AI_KEY = os.environ.get("NARA_KEY")
AI_MODEL = "mistral-large"
# mistral-large
# "mimo-v2.5-pro-free"
AI_BASE_URL = "https://router.bynara.id/v1"
# https://api.gapgpt.app/v1
# https://router.bynara.id/v1
# Support Contacts
SUPPORT_EMAIL = "Samadi.amirmohammad97@gmail.com"
SUPPORT_ID = "@GraceA_Ls"
SUPPORT_CONTACT = "@CortexShadow"
