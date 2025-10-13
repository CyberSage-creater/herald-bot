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

if __name__ == "__main__":
    logging.info("Herald starting…")
    app = ApplicationBuilder().token(TOKEN).build()
    app.post_init = _on_start
    app.run_polling()
