from pyrogram import Client

# Telegram API sozlamalari
API_ID = '9282240'
API_HASH = '493108d78871eb13b7bf13c9f23ca2de'
PHONE_NUMBER = '+998953770309'

# Session yaratish
app = Client("my_session", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

async def main():
    try:
        await app.start()
        print("Session muvaffaqiyatli yaratildi! Botni to'xtatish uchun Ctrl+C ni bosing.")
        await app.idle()
    except Exception as e:
        print(f"Xato: {e}")

if __name__ == '__main__':
    app.run(main())