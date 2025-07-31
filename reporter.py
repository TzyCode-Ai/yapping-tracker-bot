# reporter.py

import pytz
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database import get_database
from config import REPORT_RECEIVER, DAILY_REPORT_HOUR, DAILY_RESET_HOUR

logger = logging.getLogger(__name__)
db = get_database()
daily_collection = db["daily_messages"]
weekly_collection = db["weekly_totals"]

# Get Asia/Jakarta timezone
timezone = pytz.timezone("Asia/Jakarta")

# ✨ Format laporan pakai username
async def format_report(data, clients):
    if not data:
        return "📊 Tidak ada pesan terkirim hari ini."

    report = "📊 *Laporan Harian Jumlah Pesan:*\n"
    grouped = {}

    for item in data:
        key = (item["user_id"], item["chat_id"])
        grouped.setdefault(key, 0)
        grouped[key] += item["count"]

    for (user_id, chat_id), count in grouped.items():
        username = None
        for client in clients:
            try:
                user = await client.get_entity(user_id)
                if user.username:
                    username = f"@{user.username}"
                elif user.first_name or user.last_name:
                    username = f"{user.first_name or ''} {user.last_name or ''}".strip()
                else:
                    username = f"User {user.id}"
                break
            except Exception as e:
                logger.warning(f"⚠️ Gagal ambil entity {user_id}: {e}")
                username = f"User {user_id}"
        
        report += f"- 👤 {username} di Grup {chat_id}: {count} pesan\n"

    return report

# Kirim laporan ke @AimTzy18
async def send_report(clients):
    now = datetime.now(timezone)
    start = datetime(now.year, now.month, now.day, tzinfo=timezone)
    end = start.replace(hour=23, minute=59, second=59)

    data = list(daily_collection.find({
        "timestamp": {"$gte": start, "$lte": end}
    }))

    message = await format_report(data, clients)

    for client in clients:
        try:
            await client.send_message(REPORT_RECEIVER, message)
        except Exception as e:
            logger.error(f"❌ Gagal kirim laporan dari {client.session.filename}: {e}")

# Reset data harian dan update total mingguan
def reset_daily_data(now):
    data = list(daily_collection.find())

    for item in data:
        user_id = item["user_id"]
        chat_id = item["chat_id"]
        count = item["count"]

        weekly_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$inc": {"total": count}},
            upsert=True
        )

    daily_collection.delete_many({})  # Reset harian
    logger.info("✅ Data harian direset dan ditambahkan ke total mingguan.")

# Jadwalkan semua job
def schedule_jobs(clients):
    scheduler = AsyncIOScheduler(timezone=timezone)

    scheduler.add_job(
        send_report,
        CronTrigger(hour=DAILY_REPORT_HOUR, minute=0),
        args=[clients],
        name="Kirim laporan harian"
    )

    scheduler.add_job(
        reset_daily_data,
        CronTrigger(hour=DAILY_RESET_HOUR, minute=0),
        name="Reset data harian"
    )

    scheduler.start()
    logger.info("🕒 Scheduler aktif: laporan & reset terjadwal.")
