
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

    # فقط پیام‌های خصوصی
    if not event.is_private:
        return

    # =========================
    # دستور /ask
    # =========================

    # فقط پیام‌هایی که خود اکانت ارسال کرده
    if event.out:

        message = event.raw_text.strip()

        # بررسی اینکه پیام با /ask شروع شده
        if message.startswith("/ask "):

            parts = message.split(maxsplit=2)

            # فرمت صحیح:
            # /ask @username message
            if len(parts) < 3:
                print("Invalid /ask format.")
                return

            command = parts[0]
            username = parts[1]
            text = parts[2].strip()

            if not username.startswith("@"):
                print("Invalid username. Use @username")
                return

            if not text:
                print("Message text is empty.")
                return

            print("\n========== ASK COMMAND ==========")
            print("Target:", username)
            print("Message:", text)

            try:

                # پیدا کردن کاربر مقصد
                entity = await client.get_entity(username)

                # ارسال پیام
                await client.send_message(
                    entity,
                    text
                )

                print("Message sent successfully.")

            except Exception as e:
                print("ASK ERROR:", repr(e))

            print("=================================\n")

        # تمام پیام‌های خروجی خود اکانت
        # به n8n ارسال نمی‌شوند
        return


    # =========================
    # پیام‌های دریافتی
    # =========================

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

        # بررسی موفق بودن درخواست
        if response.status_code != 200:
            print("n8n request failed.")
            return

        # تبدیل پاسخ n8n به JSON
        data = response.json()

        # گرفتن جواب AI
        reply = data.get("reply", "").strip()

        if not reply:
            print("No reply received from n8n.")
            return

        # ارسال جواب به همان شخص
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

