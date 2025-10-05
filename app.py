import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "🌱 Herald test app is awake.")

async def stats_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) stats handler reached ✅")

async def ping_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "pong 🌱")

async def scroll_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) scroll handler reached ✅")

async def blessing_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) blessing handler reached ✅")

async def morning_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) morning handler reached ✅")

async def afternoon_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) afternoon handler reached ✅")

async def evening_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) evening handler reached ✅")

async def testpost_cmd(u, c):
    await c.bot.send_message(u.effective_chat.id, "(test) broadcast reached ✅")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("scroll", scroll_cmd))
    app.add_handler(CommandHandler("blessing", blessing_cmd))
    app.add_handler(CommandHandler("morning", morning_cmd))
    app.add_handler(CommandHandler("afternoon", afternoon_cmd))
    app.add_handler(CommandHandler("evening", evening_cmd))
    app.add_handler(CommandHandler("testpost", testpost_cmd))

    app.run_polling(allowed_updates=None)

if __name__ == "__main__":
    main()
