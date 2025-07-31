# tracker.py

from telethon import events
from config import TRACKED_GROUPS
from database import track_message
import logging

# Inisialisasi logger (opsional, tapi sangat berguna)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handler pesan keluar
def register_tracker(client):
    @client.on(events.NewMessage(outgoing=True))
    async def handle_outgoing_message(event):
        try:
            if not event.is_group:
                return

            chat = await event.get_chat()
            chat_id = chat.id
            chat_username = getattr(chat, "username", None)

            if chat_username and chat_username in TRACKED_GROUPS:
                user = await client.get_me()
                logger.info(f"Tracking message from {user.id} in {chat_username}")
                track_message(user_id=user.id, chat_id=chat_id, date=event.date)

        except Exception as e:
            logger.error(f"Error in handle_outgoing_message: {e}")
