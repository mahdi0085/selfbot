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

    # اگر پیام عکس نیست، کاری نکن
    if not event.photo:
        return

    # عکس‌هایی که خودمان فرستادیم را دوباره ذخیره نکن
    if event.out:
        return

    try:
        print("Photo received.")

        await client.send_file(
            "me",
            event.photo
        )

        print("Photo saved to Saved Messages.")

    except Exception as e:
        print(f"Error saving photo: {e}")


async def main():

    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()