import os
from telethon import TelegramClient

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

client = TelegramClient("/data/selfbot", API_ID, API_HASH)

async def main():
    print("Self-bot is starting...")

    me = await client.get_me()

    print(f"Logged in as: {me.first_name}")
    print("Self-bot is running...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()