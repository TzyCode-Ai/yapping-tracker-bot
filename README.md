# 📊 Telegram Yapping Tracker Bot

This is a 24/7 Telegram bot built with **Telethon** and **MongoDB** to track outgoing messages (yapping) in specified groups. The bot supports multiple accounts, daily reporting, and weekly resets.

## 🔧 Features

- ✅ Multi-account support
- ✅ Tracks outgoing messages per user per group
- ✅ Daily report at 23:59 WIB to admin
- ✅ Weekly data reset (at 01:00 WIB every Monday)
- ✅ Optional chart generation for weekly summaries
- ✅ Auto start and persistent MongoDB storage

## 📁 Folder Structure

.
├── main.py # Bot entry point
├── tracker.py # Message tracking logic
├── database.py # MongoDB access and queries
├── reporter.py # Reporting and scheduling
├── config.py # API and DB config
├── sessions/ # Session files per Telegram account
├── .env # API keys and secrets
├── .gitignore
└── README.md

## ⚙️ Requirements

- Python 3.8+
- MongoDB (local or remote)
- Telethon
- APScheduler
- matplotlib (optional, for charts)

## 📦 Installation

### 1. Clone this repository

```bash
git clone https://github.com/TzyCode-Ai/yapping-tracker-bot
cd bot-telegram-tracker
2. Install dependencies

pip install -r requirements.txt
3. Setup .env file
Create a .env file with the following content:

API_ID=your_api_id
API_HASH=your_api_hash
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/dbname
REPORT_RECEIVER=@YourTelegramUsername
4. Run the bot

python main.py
You will be prompted to login each Telegram account during the first run. Sessions will be saved in the sessions/ folder.

🕓 Scheduled Tasks
23:59 WIB: Send report to REPORT_RECEIVER

01:00 WIB: Reset daily data, keep weekly summary

Every message: increment user’s yapping count in MongoDB

🖼️ Sample Chart (optional)
You can enable chart generation in reporter.py by uncommenting the relevant section. This requires matplotlib.

📄 License
MIT License – Use freely, modify, and contribute.

💬 Contact
Maintained by AimTzy – Donate me : 0x0E6557CbA04Bc8213b1FB03b40E5dE851A7CE137(eth)
