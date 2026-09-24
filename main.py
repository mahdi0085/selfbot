import os
import tempfile

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

    # فقط عکس یا تصویر
    if not event.photo and not event.message.document:
        return

    # اگر document است، فقط image/* را قبول کن
    if event.message.document:

        mime_type = event.message.document.mime_type

        if not mime_type or not mime_type.startswith("image/"):
            return

    print("PRIVATE IMAGE DETECTED")

    temp_file = None

    try:

        # دانلود عکس روی دیسک موقت
        temp_file = await event.download_media()

        if not temp_file:
            print("IMAGE DOWNLOAD FAILED")
            return

        print("IMAGE DOWNLOADED")

        # ارسال فایل دانلودشده به Saved Messages
        await client.send_file(
            "me",
            temp_file
        )

        print("IMAGE SAVED TO SAVED MESSAGES")

    except Exception as e:

        print("PHOTO SAVE ERROR:", repr(e))

    finally:

        # حذف فایل موقت
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected() 