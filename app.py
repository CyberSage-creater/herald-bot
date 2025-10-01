import os
import json
from datetime import time, datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ── Config from env ────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))  # optional for scheduled posts
TIMEZONE = os.getenv("TIMEZONE", "America/Vancouver")
SCROLLS_PATH = os.getenv("SCROLLS_PATH", "./herald_scrolls.json")

MORNING_TIME = os.getenv("MORNING_TIME", "09:00")
AFTERNOON_TIME = os.getenv("AFTERNOON_TIME", "13:00")
EVENING_TIME = os.getenv("EVENING_TIME", "20:00")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required (set env var).")

# ── Load scrolls (JSON structure shown below) ──────────────────────────────────
with open(SCROLLS_PATH, "r", encoding="utf-8") as f:
    SCROLLS = json.load(f)

TZ = ZoneInfo(TIMEZONE)

def day_index_today() -> int:
    """Return 0..6 based on local weekday (Mon=0 ... Sun=6)."""
    return datetime.now(TZ).weekday()

async def get_member_count(context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fetch live member count for CHAT_ID; returns 0 if not available."""
    try:
        return await context.bot.get_chat_member_count(CHAT_ID)
    except Exception:
        return 0

def render_scroll(lines: list[str], member_count: int) -> str:
    return "\n".join([line.replace("[X]", str(member_count)) for line in lines])

async def post_deck(context: ContextTypes.DEFAULT_TYPE, deck_name: str):
    if CHAT_ID == 0:
        # Nothing to post to; just skip
        return
    idx = day_index_today()
    lines = SCROLLS[deck_name][idx]
    members = await get_member_count(context)
    text = render_scroll(lines, members)
    await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)

# ── JobQueue callbacks ─────────────────────────────────────────────────────────
async def post_morning(context: ContextTypes.DEFAULT_TYPE):
    await post_deck(context, "morning")

async def post_afternoon(context: ContextTypes.DEFAULT_TYPE):
    await post_deck(context, "afternoon")

async def post_evening(context: ContextTypes.DEFAULT_TYPE):
    await post_deck(context, "evening")

# ── Commands ───────────────────────────────────────────────────────────────────
async def whereami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    title = chat.title or "(no title — likely a DM)"
    await update.message.reply_text(f"Chat title: {title}\nChat ID: {chat.id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Herald online. Try /whereami 🌱⚡")

# ── Main ───────────────────────────────────────────────────────────────────────
def _parse_hhmm(s: str) -> time:
    h, m = map(int, s.split(":"))
    return time(hour=h, minute=m, tzinfo=TZ)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("whereami", whereami))

    # Scheduling (only if CHAT_ID provided)
    if CHAT_ID != 0:
        m_t = _parse_hhmm(MORNING_TIME)
        a_t = _parse_hhmm(AFTERNOON_TIME)
        e_t = _parse_hhmm(EVENING_TIME)

        app.job_queue.run_daily(post_morning, time=m_t, name="morning")
        app.job_queue.run_daily(post_afternoon, time=a_t, name="afternoon")
        app.job_queue.run_daily(post_evening, time=e_t, name="evening")

    app.run_polling()

if __name__ == "__main__":
    main()
