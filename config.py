# config.py

from dotenv import load_dotenv
import os

load_dotenv()

# Secrets
SMTP_EMAIL = os.getenv("GMAIL_EMAIL")
SMTP_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Multiple Telegram chat IDs (strings or ints both work)
TELEGRAM_CHAT_IDS = [
    os.getenv("TELEGRAM_CHAT_ID"),     # your own chat
    # "-1001234567890",                # group chat (example)
    # "987654321",                     # another user
    "telegram-chat-id", # param
    "telegram-chat-id"  # sanika
]

# Config
CHECK_INTERVAL = 60
DNS_TIMEOUT = 3
ALERT_COOLDOWN = 300
DOMAINS_FILE = "domains.json"

ALERT_TO_EMAILS = [
    "param@gmail.com"
]