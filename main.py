# main.py

import os
import asyncio
from telethon import TelegramClient
from tracker import register_tracker
from reporter import schedule_jobs
from config import API_ID, API_HASH

SESSIONS_FOLDER = "accounts"

def prompt_total_accounts():
    while True:
        try:
            count = int(input("🔢 Masukkan jumlah akun Telegram yang ingin digunakan: "))
            if count > 0:
                return count
        except ValueError:
            pass
        print("❌ Input tidak valid. Masukkan angka lebih dari 0.")

async def login_account(index: int, api_id: int, api_hash: str) -> TelegramClient:
    session_path = os.path.join(SESSIONS_FOLDER, f"account{index+1}")
    client = TelegramClient(session_path, api_id, api_hash)

    try:
        await client.connect()
        if not await client.is_user_authorized():
            print(f"🔐 Login akun ke-{index+1} (belum terautentikasi)...")
            await client.start()
        else:
            print(f"✅ Akun ke-{index+1} sudah login.")
    except Exception as e:
        print(f"⚠️ Gagal login akun ke-{index+1}: {e}")
        await client.disconnect()
        return None

    return client

async def main():
    if not os.path.exists(SESSIONS_FOLDER):
        os.makedirs(SESSIONS_FOLDER)

    account_count = prompt_total_accounts()
    clients = []

    for i in range(account_count):
        max_attempts = 2
        attempts = 0
        while attempts < max_attempts:
            client = await login_account(i, API_ID, API_HASH)
            if client:
                register_tracker(client)
                clients.append(client)
                break
            else:
                attempts += 1
                print(f"🔁 Coba login ulang untuk akun ke-{i+1}... ({attempts}/{max_attempts})\n")

        if attempts == max_attempts:
            choice = input(f"❓ Gagal 2x login akun ke-{i+1}. Mau coba ulangin nomor HP? (y/n): ").strip().lower()
            if choice == "y":
                # Hapus session file agar login ulang pakai nomor HP baru
                session_path = os.path.join(SESSIONS_FOLDER, f"account{i+1}.session")
                if os.path.exists(session_path):
                    os.remove(session_path)
                    print(f"🧹 Session akun ke-{i+1} dihapus. Ulangi login...")
                # Ulangi loop login
                client = await login_account(i, API_ID, API_HASH)
                if client:
                    register_tracker(client)
                    clients.append(client)
                else:
                    print(f"⛔ Skip akun ke-{i+1}. Gagal login.")
            else:
                print(f"⛔ Melewati akun ke-{i+1}. Tidak login.")

    if not clients:
        print("❌ Tidak ada akun yang berhasil login. Bot dihentikan.")
        return

    schedule_jobs(clients)

    print("🚀 Bot berjalan. Tracking dimulai...\n")
    await asyncio.gather(*(client.run_until_disconnected() for client in clients))

if __name__ == "__main__":
    asyncio.run(main())
