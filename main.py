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

SETTINGS_URL = "https://mehdi342.app.n8n.cloud/webhook/selfbot/settings"


def get_photo_save():
    response = requests.get(
        SETTINGS_URL,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["photo_save"]


# =========================
# Message Handler
# =========================

@client.on(events.NewMessage)
async def new_message(event):

    # فقط PV
    if not event.is_private:
        return

    # پیام‌های خودمان را نادیده بگیر
    if event.out:
        return

    # فقط وقتی روی یک پیام Reply شده
    if not event.is_reply:
        return

    try:
        replied_message = await event.get_reply_message()

        if not replied_message:
            return

        # فقط عکس
        if not replied_message.photo:
            return

        print("\n========== PHOTO TEST ==========")
        print("Message ID:", replied_message.id)
        print("Photo ID:", replied_message.photo.id)

        # =========================
        # دریافت وضعیت از n8n
        # =========================

        photo_save = get_photo_save()

        print("Photo save:", photo_save)

        if not photo_save:
            print("Photo saving is disabled.")
            print("================================\n")
            return

        # =========================
        # گرفتن نسخه تازه پیام
        # =========================

        fresh_message = await client.get_messages(
            event.chat_id,
            ids=replied_message.id
        )

        print("Fresh message loaded.")

        if not fresh_message or not fresh_message.photo:
            print("Fresh photo not found.")
            return

        print("Fresh Photo ID:", fresh_message.photo.id)

        print(
            "Fresh file_reference:",
            fresh_message.photo.file_reference
        )

        # =========================
        # Download
        # =========================

        file_path = await client.download_media(
            fresh_message
        )

        print("Downloaded:", file_path)

        if not file_path:
            print("DOWNLOAD FAILED")
            return

        # =========================
        # Saved Messages
        # =========================

        await client.send_file(
            "me",
            file_path
        )

        print("SAVED TO SAVED MESSAGES")

        # =========================
        # Delete temporary file
        # =========================

        try:
            os.remove(file_path)
        except Exception:
            pass

        print("================================\n")

    except Exception as e:
        print("ERROR:", repr(e))


# =========================
# Main
# =========================

async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    print("Self-bot is running...")


# =========================
# Start
# =========================

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()