import os
import logging
from datetime import datetime, time
from zoneinfo import ZoneInfo
from random import choice
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# — ENV —
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
TZ = os.getenv("TIMEZONE", "America/Vancouver")

# Support either a single CHANNEL_ID or a comma-separated TARGET_IDS
_channel_id_str = os.getenv("CHANNEL_ID", "").strip()
_target_ids_str = os.getenv("TARGET_IDS", "").strip()

def parse_target_ids() -> list[int]:
    ids: list[int] = []
    if _target_ids_str:
        for part in _target_ids_str.split(","):
            part = part.strip()
            if part:
                ids.append(int(part))
    elif _channel_id_str:
        ids.append(int(_channel_id_str))
    return ids

TARGET_IDS = parse_target_ids()

if not BOT_TOKEN:
    raise RuntimeError("Missing token: set TELEGRAM_BOT_TOKEN or BOT_TOKEN")
if not TARGET_IDS:
    raise RuntimeError("Missing TARGET IDS: set TARGET_IDS (comma-separated) or CHANNEL_ID")

# ── LOGGING ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("herald")

# ── 21 SCROLL DECKS ─────────────────────────────────────────────────────────────
MORNING_DECK = [
    "The dawn awakens the Grove.\n🌳 Members: [X]\n✨ May kindness bloom like wildflowers today.\n🌱 Hope stirs like dew upon the leaves.\n🍂",
    "Light breaks the horizon.\n🌳 Members: [X]\n✨ Carry kindness as petals carry color.\n🌱 Hope hums in the quiet between breaths.\n🍂",
    "Morning flows like water down the mountain.\n🌳 Members: [X]\n✨ Be gentle, as the river is with stone.\n🌱 Hope is the current unseen, carrying us forward.\n🍂",
    "The Grove whispers at dawn.\n🌳 Members: [X]\n✨ One act can echo as seven tomorrow.\n🌱 Hope glimmers like sunrise through branches.\n🍂",
    "Shadows retreat. The Grove remembers light.\n🌳 Members: [X]\n✨ Your words can be seeds today.\n🌱 Hope rises like birds from the canopy.\n🍂",
    "Roots drink the gold of morning.\n🌳 Members: [X]\n✨ Kindness is water; pour it freely.\n🌱 Hope warms the soil.\n🍂",
    "Dew beads on every leaf.\n🌳 Members: [X]\n✨ Let your step be soft and sure.\n🌱 Hope begins again.\n🍂",
]

AFTERNOON_DECK = [
    "Noon stands like a tall tree.\n🔥 Resilience breathes in the heat.\n✨ Be steady as stone, gentle as water.",
    "The sun climbs; the heart steadies.\n🪵 Wisdom listens for the quiet answer.\n✨ Choose the next right step.",
    "Wind moves through the branches.\n🔥 Scars become rings of strength.\n✨ Walk on.",
    "Midday fire, tempered by knowing.\n🧭 Wisdom marks the path; Resilience walks it.\n✨ Keep rhythm.",
    "Clouds pass. Focus remains.\n🔥 What is rooted does not fear the gust.\n✨ You are rooted.",
    "Tools in hand, breath in chest.\n🪵 Practice turns sparks into flame.\n✨ Small actions, great growth.",
    "Between hours, a still pool.\n🧭 Listen. Then act.\n✨ One clear move forward.",
]

EVENING_DECK = [
    "The light thins to silver.\n🌙 Patience counts the stars.\n✨ Harmony gathers what the day has sown.",
    "Night folds the Grove in velvet.\n🌙 Quiet isn’t empty; it is full.\n✨ Rest like roots in deep soil.",
    "Crickets keep time with the moon.\n🌙 Wait with kindness for yourself.\n✨ Tomorrow will ripen.",
    "Lanterns of memory along the path.\n🌙 You carried the day.\n✨ Set it down; let it glow.",
    "Mist lifts from the creek.\n🌙 Breathe slow; the Grove breathes with you.\n✨ Soft power endures.",
    "Branches write constellations against the dark.\n🌙 Trust the long arc.\n✨ Harmony returns in circles.",
    "The world becomes a hush of leaves.\n🌙 Patience is not pause—it is presence.",
]

# ── HELPERS ─────────────────────────────────────────────────────────────────────
def period_now(tz: str) -> str:
    now = datetime.now(ZoneInfo(tz)).time()
    if time(5, 0) <= now < time(12, 0):
        return "morning"
    if time(12, 0) <= now < time(18, 0):
        return "afternoon"
    return "evening"

def pick_scroll(tz: str) -> tuple[str, str]:
    p = period_now(tz)
    deck = MORNING_DECK if p == "morning" else AFTERNOON_DECK if p == "afternoon" else EVENING_DECK
    return p, choice(deck)

async def send_to_targets(text: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    for chat_id in TARGET_IDS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
            log.info("Sent to %s", chat_id)
        except Exception as e:
            log.exception("Failed to send to %s: %s", chat_id, e)

# ── COMMANDS ────────────────────────────────────────────────────────────────────
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Herald is awake 🌱⚡")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    p, text = pick_scroll(TZ)
    await update.message.reply_text(f"({p})\n\n{text}")

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    p, text = pick_scroll(TZ)
    await send_to_targets(f"{text}", context)
    await update.message.reply_text(f"Posted a {p} scroll to {len(TARGET_IDS)} target(s).")

# ── APP ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("now", now))
    app.add_handler(CommandHandler("post", post))
    app.run_polling()

if __name__ == "__main__":
    main()
