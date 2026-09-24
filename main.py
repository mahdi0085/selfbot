import os

from telethon import TelegramClient, events


API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

client = TelegramClient(
    "/data/selfbot",
    API_ID,
    API_HASH
)


@client.on(events.NewMessage)
async def new_message(event):

    # فقط PV
    if not event.is_private:
        return

    # پیام‌های ارسالی خودمان را نادیده بگیر
    if event.out:
        return

    # فقط رسانه‌های تصویری
    if not event.photo and not event.message.document:
        return

    # اگر document است، مطمئن شو واقعاً تصویر است
    if event.message.document:
        mime_type = event.message.document.mime_type

        if not mime_type or not mime_type.startswith("image/"):
            return

    print("PRIVATE IMAGE DETECTED")

    try:
        await client.send_file(
            "me",
            event.message.media
        )

        print("PRIVATE IMAGE SAVED TO SAVED MESSAGES")

    except Exception as e:
        print(f"PHOTO SAVE ERROR: {e}")


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()