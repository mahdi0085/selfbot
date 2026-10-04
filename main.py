
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

    # فقط وقتی روی یک پیام Reply شده
    if not event.is_reply:
        return

    try:
        replied_message = await event.get_reply_message()

        if not replied_message:
            return

        # فقط عکس و ویدیو
        if not replied_message.photo and not replied_message.video:
            return

        print("\n========== MEDIA TEST ==========")
        print("Message ID:", replied_message.id)

        if replied_message.photo:
            print("Photo ID:", replied_message.photo.id)

        if replied_message.video:
            print("Video ID:", replied_message.video.id)

        # پیام را با ID دوباره از Telegram می‌گیریم
        fresh_message = await client.get_messages(
            event.chat_id,
            ids=replied_message.id
        )

        print("Fresh message loaded.")

        if not fresh_message:
            print("Fresh media not found.")
            return

        if not fresh_message.photo and not fresh_message.video:
            print("Fresh media not found.")
            return

        if fresh_message.photo:
            print("Fresh Photo ID:", fresh_message.photo.id)
            print(
                "Fresh file_reference:",
                fresh_message.photo.file_reference
            )

        if fresh_message.video:
            print("Fresh Video ID:", fresh_message.video.id)

        # دانلود مستقیم عکس یا ویدیو
        file_path = await client.download_media(
            fresh_message
        )

        print("Downloaded:", file_path)

        if not file_path:
            print("DOWNLOAD FAILED")
            return

        # ارسال فایل دانلودشده به Saved Messages
        await client.send_file(
            "me",
            file_path
        )

        print("SAVED TO SAVED MESSAGES")

        # حذف فایل موقت
        try:
            os.remove(file_path)
        except Exception:
            pass

        print("================================\n")

    except Exception as e:
        print("ERROR:", repr(e))


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
