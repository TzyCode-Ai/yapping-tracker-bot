# database.py

from pymongo import MongoClient
from datetime import datetime, timedelta
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

daily_collection = db["daily_messages"]
weekly_collection = db["weekly_totals"]

def track_message(user_id: int, chat_id: int, date: datetime):
    today = date.strftime("%Y-%m-%d")

    # Tambah ke harian
    daily_collection.update_one(
        {"user_id": user_id, "chat_id": chat_id, "date": today},
        {"$inc": {"count": 1}},
        upsert=True
    )

    # Tambah juga ke total mingguan
    week_start = (date - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
    weekly_collection.update_one(
        {"user_id": user_id, "chat_id": chat_id, "week_start": week_start},
        {"$inc": {"count": 1}},
        upsert=True
    )

def get_daily_report(date: datetime):
    today = date.strftime("%Y-%m-%d")
    return list(daily_collection.find({"date": today}))

def reset_daily_data(date: datetime):
    today = date.strftime("%Y-%m-%d")
    daily_collection.delete_many({"date": today})

def get_weekly_totals():
    return list(weekly_collection.find())
