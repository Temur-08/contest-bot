from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# API sozlamalari
API_ID = '9282240'
API_HASH = '493108d78871eb13b7bf13c9f23ca2de'
SESSION_FILE = 'my_session.session'

# Bot
app = Client(SESSION_FILE, api_id=API_ID, api_hash=API_HASH)
CHAT_ID = None
WORD_TO_SEND = None
IS_RUNNING = False

# /start
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    global IS_RUNNING
    IS_RUNNING = False
    await message.reply(
        "Bot tayyor! Chat ID va so‘z kiriting.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Chat ID", callback_data="set_chat_id")],
            [InlineKeyboardButton("So‘z", callback_data="set_word")],
            [InlineKeyboardButton("Boshlash", callback_data="start_monitoring")]
        ])
    )

# Knopkalar
@app.on_callback_query()
async def handle_callback(client, callback_query):
    global CHAT_ID, WORD_TO_SEND, IS_RUNNING
    data = callback_query.data
    if data == "set_chat_id":
        await callback_query.message.reply("Chat ID kiriting (masalan, -100123456789):")
        app.set_chat_id_mode = True
    elif data == "set_word":
        await callback_query.message.reply("So‘z kiriting (masalan, salom):")
        app.set_word_mode = True
    elif data == "start_monitoring":
        if CHAT_ID is None or WORD_TO_SEND is None:
            await callback_query.message.reply("Chat ID va so‘z kerak!")
        else:
            IS_RUNNING = True
            await callback_query.message.reply("Kuzatuv boshlandi!")
            asyncio.create_task(monitor_chat())

# Kiritish
@app.on_message(filters.private)
async def handle_input(client, message):
    global CHAT_ID, WORD_TO_SEND
    if hasattr(app, 'set_chat_id_mode') and app.set_chat_id_mode:
        try:
            CHAT_ID = int(message.text)
            app.set_chat_id_mode = False
            await message.reply(f"Chat ID: {CHAT_ID}")
        except ValueError:
            await message.reply("Noto‘g‘ri ID!")
    elif hasattr(app, 'set_word_mode') and app.set_word_mode:
        WORD_TO_SEND = message.text
        app.set_word_mode = False
        await message.reply(f"So‘z: {WORD_TO_SEND}")

# Xabar yuborish
async def monitor_chat():
    while IS_RUNNING:
        try:
            await app.send_message(CHAT_ID, WORD_TO_SEND)
            print(f"So‘z yuborildi: {WORD_TO_SEND}")
            break
        except Exception as e:
            await asyncio.sleep(0.1)
            continue

# Botni ishga tushirish
async def main():
    try:
        await app.start()
        print("Bot ishga tushdi!")
        await app.idle()
    except Exception as e:
        print(f"Xato: {e}")

if __name__ == '__main__':
    app.run(main())