# ===== Herald Symbol Cycle v3.0 =====
# Dual symbols per window: (Elemental, Natural) + ready-to-use joined tag.
HERALD_SYMBOLS = {
    "morning": {
        "elemental": "☀️",
        "natural": "🌱",
        "tag": "☀️🌱",
        "line": "The dawn returns. What you tend now will grow."
    },
    "afternoon": {
        "elemental": "⚡",
        "natural": "🌿",
        "tag": "⚡🌿",
        "line": "The day endures. The Grove learns through each spark."
    },
    "evening": {
        "elemental": "🌙",
        "natural": "💧",
        "tag": "🌙💧",
        "line": "The Grove listens. What was spoken in light, rests in water."
    },
}

# Optional: allow override via env (e.g., HERALD_TZ="America/Vancouver")
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Py3.9+
except Exception:
    ZoneInfo = None

HERALD_TZ = os.getenv("HERALD_TZ", "America/Vancouver")

def _now_local():
    if ZoneInfo:
        return datetime.now(ZoneInfo(HERALD_TZ))
    # Fallback to naive local time if zoneinfo unavailable
    return datetime.now()

def infer_period_from_now(dt=None):
    """
    Returns one of: 'morning', 'afternoon', 'evening'
    Morning: 05;
    """
import os
import logging
from telegram.ext import ApplicationBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s"
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TARGET_IDS = [int(x) for x in os.environ["TARGET_IDS"].split(",")]

async def _on_start(app):
    # Smoke post so we know the bot really booted
    for cid in TARGET_IDS:
        try:
            await app.bot.send_message(chat_id=cid, text="🌱 Herald has awakened.")
            logging.info("Startup post sent to %s", cid)
        except Exception:
            logging.exception("Startup post failed for %s", cid)
# --- Manual scroll request system -----------------------------------
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

MENU = [["🌅 Morning", "⚡ Afternoon", "🌙 Evening"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Welcome to the Grove.\nChoose a time to receive a scroll:",
        reply_markup=ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    )

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "morning" in text:
        period = "morning"
    elif "afternoon" in text:
        period = "afternoon"
    elif "evening" in text:
        period = "evening"
    else:
        await update.message.reply_text("I don’t know that scroll yet 🌱")
        return

    msg = build_scroll(period)
    await update.message.reply_text(msg, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type /menu to request a Grove scroll 🌿")

# -----------------------------------------------------------

if __name__ == "__main__":
    logging.info("Herald starting…")
    app = ApplicationBuilder().token(TOKEN).build()
    app.post_init = _on_start

    # Add handlers here
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# inline menu
async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🌅 Morning", callback_data="scroll:morning")],
        [InlineKeyboardButton("⚡ Afternoon", callback_data="scroll:afternoon")],
        [InlineKeyboardButton("🌙 Evening", callback_data="scroll:evening")],
    ]
    await update.message.reply_text(
        "🌱 Choose a Grove scroll:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# handle button clicks
async def menu_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    period = query.data.split(":")[1]
    msg = build_scroll(period)   # your existing JSON-backed function
    await query.message.reply_text(msg, parse_mode="Markdown")

if __name__ == "__main__":
    logging.info("Herald starting…")
    app = ApplicationBuilder().token(TOKEN).build()
    app.post_init = _on_start

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_cmd))

    # inline button handler
    app.add_handler(CallbackQueryHandler(menu_pick, pattern=r"^scroll:(morning|afternoon|evening)$"))

    app.run_polling()
