from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# Telegram API sozlamalari
API_ID = 'YOUR_API_ID'  # my.telegram.org dan oling
API_HASH = 'YOUR_API_HASH'  # my.telegram.org dan oling
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'  # Telegram hisobingiz raqami

# Bot sozlamalari
app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
CHAT_ID = None  # Guruh chat ID’si
WORD_TO_SEND = None  # Yuboriladigan so‘z
IS_RUNNING = False  # Bot kuzatuv holati

# /start buyrug‘i
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    global IS_RUNNING
    IS_RUNNING = False
    await message.reply(
        "Bot ishga tushdi! Guruh chat ID’sini va so‘zni kiritish uchun knopkalarni ishlating.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Chat ID kiritish", callback_data="set_chat_id")],
            [InlineKeyboardButton("So‘z kiritish", callback_data="set_word")],
            [InlineKeyboardButton("Davom etish", callback_data="start_monitoring")]
        ])
    )

# Knopka bosilganda
@app.on_callback_query()
async def handle_callback(client, callback_query):
    global CHAT_ID, WORD_TO_SEND, IS_RUNNING
    data = callback_query.data

    if data == "set_chat_id":
        await callback_query.message.reply("Guruh chat ID’sini yuboring (masalan, -100123456789):")
        app.set_chat_id_mode = True
    elif data == "set_word":
        await callback_query.message.reply("Yuboriladigan so‘zni yuboring (masalan, salom):")
        app.set_word_mode = True
    elif data == "start_monitoring":
        if CHAT_ID is None or WORD_TO_SEND is None:
            await callback_query.message.reply("Iltimos, avval chat ID va so‘zni kiriting!")
        else:
            IS_RUNNING = True
            await callback_query.message.reply("Kuzatuv boshlandi! Guruh ruxsati ochilishi kutilmoqda...")
            asyncio.create_task(monitor_chat())

# Chat ID va so‘zni qabul qilish
@app.on_message(filters.private)
async def handle_input(client, message):
    global CHAT_ID, WORD_TO_SEND
    if hasattr(app, 'set_chat_id_mode') and app.set_chat_id_mode:
        try:
            CHAT_ID = int(message.text)
            app.set_chat_id_mode = False
            await message.reply(f"Chat ID saqlandi: {CHAT_ID}")
        except ValueError:
            await message.reply("Noto‘g‘ri chat ID! Iltimos, raqamli formatda kiriting (masalan, -100123456789).")
    elif hasattr(app, 'set_word_mode') and app.set_word_mode:
        WORD_TO_SEND = message.text
        app.set_word_mode = False
        await message.reply(f"So‘z saqlandi: {WORD_TO_SEND}")

# Guruh ruxsatini kuzatish
async def monitor_chat():
    while IS_RUNNING:
        try:
            # Sinov xabari yuborish
            await app.send_message(CHAT_ID, WORD_TO_SEND)
            print(f"So‘z yuborildi: {WORD_TO_SEND}")
            break  # Muvaffaqiyatli yuborilganda tsikldan chiqish
        except Exception as e:
            # Agar xabar yuborish muvaffaqiyatsiz bo‘lsa (ruxsat yo‘q)
            await asyncio.sleep(0.05)  # 0.05 soniya kutish
            continue

# Botni ishga tushirish
async def main():
    await app.start()
    print("Bot ishga tushdi!")
    await app.idle()

if __name__ == '__main__':
    app.run(main())