import os
import random
import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TIMEZONE = os.getenv("TIMEZONE", "America/Vancouver")

SCROLLS = [
    "🍂 Dawn whispers: Hope roots itself in you today.",
    "🔥 Noon ember: Courage rises from within.",
    "🌙 Nightfall: Patience shines in the quiet sky."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Herald online 🌱⚡")

async def bless(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scroll = random.choice(SCROLLS)
    await update.message.reply_text(scroll)

async def send_scroll(context: ContextTypes.DEFAULT_TYPE, scroll: str):
    await context.bot.send_message(chat_id=CHANNEL_ID, text=scroll)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    scheduler.add_job(send_scroll, CronTrigger(hour=9, minute=0), args=[app.bot, SCROLLS[0]])
    scheduler.add_job(send_scroll, CronTrigger(hour=13, minute=0), args=[app.bot, SCROLLS[1]])
    scheduler.add_job(send_scroll, CronTrigger(hour=20, minute=30), args=[app.bot, SCROLLS[2]])

    scheduler.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bless", bless))

    app.run_polling()

if __name__ == "__main__":
    main()
