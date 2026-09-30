import os
import json

from telethon import TelegramClient


# =====================================
# CONFIG
# =====================================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

CHANNEL_USERNAME = "@badje12"

OUTPUT_FILE = "/data/badje12_messages.jsonl"


# =====================================
# TELEGRAM CLIENT
# =====================================

client = TelegramClient(
    "/data/selfbot",
    API_ID,
    API_HASH
)


# =====================================
# EXPORT TEXT
# =====================================

async def export_channel():

    print("\n================================")
    print("Starting channel export...")
    print("Channel:", CHANNEL_USERNAME)
    print("================================\n")

    # پیدا کردن کانال
    channel = await client.get_entity(
        CHANNEL_USERNAME
    )

    print(
        "Channel:",
        getattr(channel, "title", "")
    )

    print(
        "Channel ID:",
        channel.id
    )

    # ---------------------------------
    # استخراج پیام‌ها
    # ---------------------------------

    count = 0

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        async for message in client.iter_messages(
            channel,
            reverse=True
        ):

            # فقط پیام‌هایی که متن دارند
            if not message.raw_text:
                continue

            text = message.raw_text.strip()

            if not text:
                continue

            data = {
                "message_id": message.id,

                "date": (
                    message.date.isoformat()
                    if message.date
                    else None
                ),

                "text": text
            }

            file.write(
                json.dumps(
                    data,
                    ensure_ascii=False
                )
                + "\n"
            )

            count += 1

            print(
                f"[{count}] Message ID: {message.id}"
            )

    print("\n================================")
    print("EXPORT COMPLETE")
    print("Messages:", count)
    print("File:", OUTPUT_FILE)
    print("================================\n")


# =====================================
# MAIN
# =====================================

async def main():

    print(
        "Connecting to Telegram..."
    )

    await client.start()

    me = await client.get_me()

    print(
        "Logged in as:",
        me.first_name,
        me.id
    )

    await export_channel()


# =====================================
# START
# =====================================

with client:

    client.loop.run_until_complete(
        main()
    )