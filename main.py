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

    # هر نوع پیام را بررسی می‌کنیم
    print("New message received:")
    print(event.raw_text)

    # اگر پیام عکس ندارد، کاری نکن
    if event.message.photo is None:
        return

    # اگر عکس را خود اکانت فرستاده، دوباره ذخیره نکن
    if event.out:
        return

    print("PHOTO DETECTED")

    try:
        await client.send_file(
            "me",
            event.message.photo
        )

        print("PHOTO SAVED TO SAVED MESSAGES")

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