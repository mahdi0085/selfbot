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

    # پیام‌های خودمان را نادیده بگیر
    if event.out:
        return

    print("========== PRIVATE MESSAGE ==========")
    print("Text:", event.raw_text)
    print("Media:", type(event.message.media).__name__)
    print("Photo:", event.message.photo is not None)
    print("Document:", event.message.document is not None)

    # فقط تصویر
    is_image = False

    # عکس معمولی تلگرام
    if event.message.photo is not None:
        is_image = True

    # تصویر ارسال‌شده به شکل فایل
    elif event.message.document is not None:

        mime_type = event.message.document.mime_type

        print("Document MIME:", mime_type)

        if mime_type and mime_type.startswith("image/"):
            is_image = True

    if not is_image:
        print("Not an image.")
        print("=====================================")
        return

    print("IMAGE DETECTED")

    try:

        await client.send_file(
            "me",
            event.message.media
        )

        print("IMAGE SAVED TO SAVED MESSAGES")

    except Exception as e:

        print("SAVE ERROR:", repr(e))

    print("=====================================")


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()