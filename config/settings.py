import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
API_TOKEN = os.environ.get("API_KEY")

# AI Configuration
AI_KEY = os.environ.get("AI_KEY")
GAP_API = os.environ.get("GAP_API")
AI_MODEL = "qwen3-235b-a22b"
AI_BASE_URL = "https://api.gapgpt.app/v1"

# Support Contacts
SUPPORT_EMAIL = "Samadi.amirmohammad97@gmail.com"
SUPPORT_ID = "@GraceA_Ls"
SUPPORT_CONTACT = "@CortexShadow"
