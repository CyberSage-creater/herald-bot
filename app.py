import os
import logging
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# ── ENV ─────────────────────────────────────────────────────────────────────────
BOT_TOKEN   = os.getenv("BOT_TOKEN")           # from BotFather
CHANNEL_ID  = os.getenv("CHANNEL_ID")          # e.g. -1001234567890
TZ          = os.getenv("TZ", "America/Vancouver")  # your local time zone

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN env var")
if not CHANNEL_ID:
    raise RuntimeError("Missing CHANNEL_ID env var")

CHANNEL_ID = int(CHANNEL_ID)

# ── LOGGING ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("herald")

# ── CONTENT (tiny starter deck; you can expand anytime) ─────────────────────────
MORNING = (
    "The dawn awakens the Grove.\n"
    "✨ May kindness bloom like wildflowers today.\n"
    "🌱 Hope stirs like dew upon the leaves. 🍂"
)
AFTERNOON = (
    "Fire warms the roots at noon.\n"
    "✨ Be steady as stone, gentle as water.\n"
    "🔥 Resilience remembers. 🔥"
)
EVENING = (
    "Night gathers, but the Grove glows within.\n"
    "✨ Patience counts the stars.\n"
    "🌙 Harmony breathes. 🌙"
)

# ── COMMANDS ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Herald of the Grove is awake.\n"
        "Type /scroll or /blessing — or just enjoy the daily posts.\n"
        "Take root. Rise. Grow. ⚡"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – greet the Herald\n"
        "/scroll – receive a Grove scroll now\n"
        "/blessing – a short blessing now\n"
        "/stats – quick status\n"
        "/help – this menu"
    )

async def scroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "The Grove prepares, the roots stir.\n"
        "Quiet strength gathers in the soil. 🌌",
        parse_mode=ParseMode.HTML
    )

async def blessing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ May your steps be rooted and your breath be light today."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    me = await context.bot.get_me()
    await update.message.reply_text(
        f"🤖 {me.first_name} is running.\n"
        f"⏰ TZ: {TZ}\n"
        f"📢 Channel ID: {CHANNEL_ID}"
    )

# ── SCHEDULED POSTS ─────────────────────────────────────────────────────────────
async def post_text(ctx: ContextTypes.DEFAULT_TYPE, text: str):
    await ctx.bot.send_message(chat_id=CHANNEL_ID, text=text)

async def morning_job(ctx: ContextTypes.DEFAULT_TYPE):
    await post_text(ctx, MORNING)

async def afternoon_job(ctx: ContextTypes.DEFAULT_TYPE):
    await post_text(ctx, AFTERNOON)

async def evening_job(ctx: ContextTypes.DEFAULT_TYPE):
    await post_text(ctx, EVENING)

def schedule_jobs(app):
    tz = ZoneInfo(TZ)
    jq = app.job_queue

    # 9:00am, 2:00pm, 9:00pm local time (change as you like)
    jq.run_daily(morning_job,   time(hour=9,  minute=0, tzinfo=tz), name="morning")
    jq.run_daily(afternoon_job, time(hour=14, minute=0, tzinfo=tz), name="afternoon")
    jq.run_daily(evening_job,   time(hour=21, minute=0, tzinfo=tz), name="evening")
    log.info("Jobs scheduled for %s", TZ)

# ── MAIN ────────────────────────────────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("scroll", scroll))
    app.add_handler(CommandHandler("blessing", blessing))
    app.add_handler(CommandHandler("stats", stats))

    schedule_jobs(app)
    log.info("Herald is starting (polling)…")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
