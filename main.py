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
# Telegram Messages
# =========================

@client.on(events.NewMessage)
async def new_message(event):

    print("New message received:")
    print(event.raw_text)

    # =========================
    # Ping
    # =========================

    if event.raw_text == "/ping":
        await event.reply("Pong 🟢")
        return

    # =========================
    # Photo
    # =========================

    if event.photo:

        # اگر پیام را خود اکانت فرستاده، کاری نکن
        if event.out:
            return

        # اگر پیام از PV نیست، کاری نکن
        if not event.is_private:
            print("Photo is not from private chat. Ignored.")
            return

        print("Private photo received.")

        try:
            # دریافت وضعیت از n8n
            photo_save = get_photo_save()

            print(f"Photo save setting: {photo_save}")

            if photo_save:

                # ارسال عکس به Saved Messages
                await client.send_file(
                    "me",
                    event.photo
                )

                print("Photo sent to Saved Messages.")

            else:
                print("Photo saving is disabled.")

        except Exception as e:
            print(f"Error while processing photo: {e}")


# =========================
# Main
# =========================

async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    # دریافت تنظیم فعلی از n8n
    photo_save = get_photo_save()

    print(f"Photo save: {photo_save}")

    print("Self-bot is running...")


# =========================
# Start
# =========================

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()