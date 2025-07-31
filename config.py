# config.py

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = "telegram_tracker"

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

REPORT_RECEIVER = "AimTzy18"

TRACKED_GROUPS = [
    "InitVerseWeb3",
    "InitVerseIndonesia",
    "MemeCoreCommunity",
]

DAILY_REPORT_HOUR = 23
DAILY_RESET_HOUR = 1
