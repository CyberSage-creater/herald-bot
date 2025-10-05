import os
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# — ENV —
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
TZ = os.getenv("TIMEZONE", "America/Vancouver")

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN")
if not CHANNEL_ID:
    raise RuntimeError("Missing CHANNEL_ID")

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
    "The world becomes a hush of leaves.\n🌙 Patience is not pause—it is presence.\n✨ Be here.",
]

BLESSINGS = [
    "✨ May your steps be rooted and your breath be light today.",
    "✨ May your words be seeds and your silence water.",
    "✨ May resilience rise in you like fire remembered.",
    "✨ May wisdom meet you in the next clear choice.",
    "✨ May kindness find you first—and then flow through you.",
    "✨ May patience widen your horizon and soften your shoulders.",
    "✨ May harmony tune your day to the quiet music of the Grove.",
]

# ── HELPERS ─────────────────────────────────────────────────────────────────────
def pick_deck_by_hour(hour: int):
    """Return deck name and list by local hour."""
    if 5 <= hour < 12:
        return "morning", MORNING_DECK
    if 12 <= hour < 18:
        return "afternoon", AFTERNOON_DECK
    return "evening", EVENING_DECK

async def send(ctx: ContextTypes.DEFAULT_TYPE, text: str, chat_id: int | None = None):
    for cid in CHANNEL_IDS:
        try:
            await bot.send_message(chat_id=cid, text=text)
        except Exception as e:
            print(f"⚠️ Failed to send to {cid}: {e}")
# ── COMMANDS ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌱 Herald of the Grove is awake.\n"
        "Type /scroll or /blessing — or enjoy the daily posts.\n"
        "Take root. Rise. Grow. ⚡"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – greet the Herald\n"
        "/scroll – receive a Grove scroll (fits the time of day)\n"
        "/blessing – a short blessing now\n"
        "/stats – quick status\n"
        "/morning /afternoon /evening – sample those decks"
    )

async def scroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = ZoneInfo(TZ)
    hour = update.effective_message.date.astimezone(tz).hour
    _, deck = pick_deck_by_hour(hour)
    await update.message.reply_text(choice(deck))

async def blessing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choice(BLESSINGS))

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    me = await context.bot.get_me()
    await update.message.reply_text(
        f"🤖 {me.first_name} running\n"
        f"⏰ TZ: {TZ}\n"
        f"📢 Channel ID: {CHANNEL_ID}"
    )

# deck samplers for testing
async def morning_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choice(MORNING_DECK))
async def afternoon_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choice(AFTERNOON_DECK))
async def evening_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choice(EVENING_DECK))

# ── SCHEDULED POSTS ─────────────────────────────────────────────────────────────
async def morning_job(ctx: ContextTypes.DEFAULT_TYPE):
    await send(ctx, choice(MORNING_DECK))
async def afternoon_job(ctx: ContextTypes.DEFAULT_TYPE):
    await send(ctx, choice(AFTERNOON_DECK))
async def evening_job(ctx: ContextTypes.DEFAULT_TYPE):
    await send(ctx, choice(EVENING_DECK))

def schedule_jobs(app):
    tz = ZoneInfo(TZ)
    jq = app.job_queue
    if jq is None:
        log.warning("JobQueue not available; skipping schedules.")
        return
    jq.run_daily(morning_job,   time(hour=9,  minute=0, tzinfo=tz), name="morning")
    jq.run_daily(afternoon_job, time(hour=14, minute=0, tzinfo=tz), name="afternoon")
    jq.run_daily(evening_job,   time(hour=21, minute=0, tzinfo=tz), name="evening")
    log.info("Jobs scheduled for %s", TZ)

# ── MAIN ────────────────────────────────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("scroll", scroll))
    app.add_handler(CommandHandler("blessing", blessing))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("morning", morning_cmd))
    app.add_handler(CommandHandler("afternoon", afternoon_cmd))
    app.add_handler(CommandHandler("evening", evening_cmd))

    schedule_jobs(app)
    log.info("Herald is starting (polling)…")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
