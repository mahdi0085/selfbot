
import os
import requests

from telethon import TelegramClient, events


# =====================================
# CONFIG
# =====================================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

N8N_WEBHOOK_URL = "https://mehdi342.app.n8n.cloud/webhook/telegram-account-ai"


# =====================================
# TELEGRAM CLIENT
# =====================================

client = TelegramClient(
    "/data/selfbot",
    API_ID,
    API_HASH
)


# =====================================
# NEW MESSAGE HANDLER
# =====================================

@client.on(events.NewMessage)
async def new_message(event):

    # فقط پیام‌های خصوصی
    if not event.is_private:
        return


    # =========================================================
    # قابلیت جدید:
    # Reply روی یک عکس → دانلود عکس → ارسال به Saved Messages
    # =========================================================

    if event.is_reply:

        try:

            replied_message = await event.get_reply_message()

            if not replied_message:
                return

            # فقط عکس
            if replied_message.photo:

                print("\n========== PHOTO TEST ==========")
                print("Message ID:", replied_message.id)
                print("Photo ID:", replied_message.photo.id)

                # ---------------------------------------------
                # دریافت مجدد پیام از Telegram
                # ---------------------------------------------

                fresh_message = await client.get_messages(
                    event.chat_id,
                    ids=replied_message.id
                )

                print("Fresh message loaded.")

                if not fresh_message or not fresh_message.photo:
                    print("Fresh photo not found.")
                    return

                print(
                    "Fresh Photo ID:",
                    fresh_message.photo.id
                )

                print(
                    "Fresh file_reference:",
                    fresh_message.photo.file_reference
                )

                # ---------------------------------------------
                # دانلود عکس
                # ---------------------------------------------

                file_path = await client.download_media(
                    fresh_message
                )

                print("Downloaded:", file_path)

                if not file_path:
                    print("DOWNLOAD FAILED")
                    return

                # ---------------------------------------------
                # ارسال به Saved Messages
                # ---------------------------------------------

                await client.send_file(
                    "me",
                    file_path
                )

                print("SAVED TO SAVED MESSAGES")

                # ---------------------------------------------
                # حذف فایل موقت
                # ---------------------------------------------

                try:
                    os.remove(file_path)
                    print("Temporary file deleted.")

                except Exception as e:
                    print(
                        "Could not delete temporary file:",
                        repr(e)
                    )

                print("================================\n")

                # ---------------------------------------------
                # مهم:
                # چون این Reply یک عکس بود، دیگر ادامه
                # ندهیم تا به n8n ارسال نشود.
                # ---------------------------------------------

                return

        except Exception as e:

            print("PHOTO ERROR:", repr(e))

            return


    # =========================================================
    # پیام‌های ارسال‌شده توسط خود اکانت
    # =========================================================

    if event.out:

        message = event.raw_text.strip()


        # ---------------------------------
        # /ask @username
        # ---------------------------------

        if message.startswith("/ask "):

            parts = message.split(maxsplit=2)


            # باید حداقل /ask و username وجود داشته باشد
            if len(parts) < 2:

                print("Usage: /ask @username")

                return


            username = parts[1]


            if not username.startswith("@"):

                print("Username must start with @")

                return


            # اگر متن سوم وجود داشته باشد،
            # همان متن را استفاده می‌کنیم.

            custom_message = (
                parts[2].strip()
                if len(parts) == 3
                else ""
            )


            print("\n========== ASK COMMAND ==========")
            print("Target:", username)


            try:

                # ---------------------------------
                # پیدا کردن شخص مقصد
                # ---------------------------------

                entity = await client.get_entity(
                    username
                )


                # ---------------------------------
                # حالت جدید:
                # /ask @username
                # ---------------------------------

                if not custom_message:

                    print(
                        "Requesting message from n8n AI..."
                    )


                    response = requests.post(
                        N8N_WEBHOOK_URL,

                        json={
                            "action": "ask",
                            "username": username
                        },

                        timeout=120
                    )


                    print(
                        "n8n Status:",
                        response.status_code
                    )

                    print(
                        "n8n Response:",
                        response.text
                    )


                    if response.status_code != 200:

                        print(
                            "n8n request failed."
                        )

                        return


                    data = response.json()


                    text_to_send = (
                        data.get("reply", "")
                        .strip()
                    )


                    if not text_to_send:

                        print(
                            "AI did not generate a message."
                        )

                        return


                # ---------------------------------
                # حالت قبلی:
                # /ask @username message
                # ---------------------------------

                else:

                    text_to_send = custom_message


                # ---------------------------------
                # ارسال پیام به شخص
                # ---------------------------------

                await client.send_message(
                    entity,
                    text_to_send
                )


                print(
                    "Message sent successfully."
                )

                print(
                    "Message:",
                    text_to_send
                )


            except Exception as e:

                print(
                    "ASK ERROR:",
                    repr(e)
                )


            print(
                "=================================\n"
            )


        # ---------------------------------
        # پیام‌های خروجی خود اکانت
        # به n8n نمی‌روند
        # ---------------------------------

        return


    # =========================================================
    # پیام‌های دریافتی از دیگران
    # =========================================================

    message = event.raw_text.strip()


    if not message:

        return


    print(
        "\n========== NEW PRIVATE MESSAGE =========="
    )

    print(
        "Chat ID:",
        event.chat_id
    )

    print(
        "Message:",
        message
    )


    try:

        response = requests.post(
            N8N_WEBHOOK_URL,

            json={
                "message": message,
                "chat_id": event.chat_id
            },

            timeout=120
        )


        print(
            "n8n Status:",
            response.status_code
        )

        print(
            "n8n Response:",
            response.text
        )


        if response.status_code != 200:

            print(
                "n8n request failed."
            )

            return


        data = response.json()


        reply = (
            data.get("reply", "")
            .strip()
        )


        if not reply:

            print(
                "No reply received from n8n."
            )

            return


        # ---------------------------------
        # ارسال پاسخ n8n
        # ---------------------------------

        await client.send_message(
            event.chat_id,
            reply
        )


        print(
            "Reply sent successfully."
        )


    except Exception as e:

        print(
            "ERROR:",
            repr(e)
        )


    print(
        "========================================\n"
    )


# =====================================
# MAIN
# =====================================

async def main():

    print(
        "Self-bot is starting..."
    )


    me = await client.get_me()


    print(
        "Self-bot is running..."
    )


# =====================================
# START CLIENT
# =====================================

with client:

    client.loop.run_until_complete(
        main()
    )

    client.run_until_disconnected()
