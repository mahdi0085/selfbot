
import os
import requests

from telethon import TelegramClient, events


API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

N8N_WEBHOOK_URL = "https://mehdi342.app.n8n.cloud/webhook-test/telegram-account-ai"

client = TelegramClient(
    "/data/selfbot",
    API_ID,
    API_HASH
)


@client.on(events.NewMessage)
async def new_message(event):

    # فقط پیام خصوصی
    if not event.is_private:
        return

    # متن پیام
    message = event.raw_text.strip()

    # پیام خالی
    if not message:
        return

    print("\n========== NEW PRIVATE MESSAGE ==========")
    print("Chat ID:", event.chat_id)
    print("Message:", message)

    try:

        # ارسال پیام به n8n
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={
                "message": message,
                "chat_id": event.chat_id
            },
            timeout=120
        )

        print("n8n Status:", response.status_code)
        print("n8n Response:", response.text)

        if response.status_code != 200:
            print("n8n request failed.")
            return

        data = response.json()

        reply = data.get("reply", "").strip()

        if not reply:
            print("No reply received from n8n.")
            return

        # ارسال جواب به همان چت
        await client.send_message(
            event.chat_id,
            reply
        )

        print("Reply sent successfully.")

    except Exception as e:
        print("ERROR:", repr(e))

    print("========================================\n")


async def main():

    print("Self-bot is starting...")

    await client.get_me()

    print("Self-bot is running...")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()

