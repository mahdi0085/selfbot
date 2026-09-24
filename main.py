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

    # فقط پیام‌هایی که Reply هستند
    if not event.is_reply:
        return

    try:
        replied_message = await event.get_reply_message()

        if not replied_message:
            return

        print("\n========== REPLIED MESSAGE INFO ==========")

        print("Message ID:", replied_message.id)
        print("Date:", replied_message.date)

        print("Text:", repr(replied_message.raw_text))

        print("Media type:", type(replied_message.media).__name__)

        print("Has photo:", replied_message.photo is not None)

        print(
            "Has document:",
            replied_message.document is not None
        )

        if replied_message.photo:
            print("Photo object:")
            print(repr(replied_message.photo))

            print("Photo ID:", replied_message.photo.id)
            print("Photo access_hash:", replied_message.photo.access_hash)
            print("Photo file_reference:", replied_message.photo.file_reference)

        if replied_message.document:
            print("Document MIME:", replied_message.document.mime_type)
            print("Document ID:", replied_message.document.id)
            print(
                "Document file_reference:",
                replied_message.document.file_reference
            )

        print("==========================================\n")

    except Exception as e:
        print("ERROR:", repr(e))


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()