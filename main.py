import os
from telethon import TelegramClient, events

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

client = TelegramClient("/data/selfbot", API_ID, API_HASH)


@client.on(events.NewMessage)
async def new_message(event):
    print("New message received:")
    print(event.raw_text)

    if event.raw_text == "/ping":
        await event.reply("Pong 🟢")


async def main():
    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")
    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()