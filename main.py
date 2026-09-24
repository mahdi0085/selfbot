import os
import requests

from telethon import TelegramClient, events


# =========================
# Telegram
# =========================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

client = TelegramClient(
    "/data/selfbot",
    API_ID,
    API_HASH
)


# =========================
# n8n Settings
# =========================

SETTINGS_URL = "https://mehdi342.app.n8n.cloud/webhook-test/selfbot/settings"


def get_photo_save():
    response = requests.get(
        SETTINGS_URL,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["photo_save"]


# =========================
# Telegram Messages
# =========================

@client.on(events.NewMessage)
async def new_message(event):
    print("New message received:")
    print(event.raw_text)

    if event.raw_text == "/ping":
        await event.reply("Pong 🟢")


# =========================
# Main
# =========================

async def main():
    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    # دریافت تنظیم از n8n
    photo_save = get_photo_save()

    print(f"Photo save: {photo_save}")

    print("Self-bot is running...")


# =========================
# Start
# =========================

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()