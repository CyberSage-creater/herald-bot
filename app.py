import os, random
from zoneinfo import ZoneInfo
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]  # e.g. "@TheGroveChannel" (bot must be admin)
TZ = ZoneInfo(os.getenv("TIMEZONE", "America/Vancouver"))

# --- Scroll decks (7 morning, 7 afternoon, 7 evening). Edit freely. ---
MORNING = [
    "🍂 Dawn blessing:\nRoots wake, light returns.\nTake root. Rise. Grow. ⚡",
    "🍂 Quiet hope gathers in the soil.\nA new day begins within. 🌱",
    "🍂 The Grove remembers.\nYou are not late. You are on time. 🌌",
    "🍂 Breathe like trees.\nIn, grow. Out, release.",
    "🍂 Small light, steady path.\nCarry it well today. ✨",
    "🍂 One shared space. One special story.\nWalk gently.",
    "🍂 Begin again.\nThe seed is enough. 🌱"
]
AFTERNOON = [
    "🔥 Midday spark:\nHold the line. Grow through. ⚡",
    "🔥 Resilience is quiet motion.\nKeep water in your roots. 💧",
    "🔥 What you tend, tends you.\nReturn to your core.",
    "🔥 Steady flame, gentle heart.\nPress on. 🌲",
    "🔥 The seventh wave is forming.\nStand ready. 🌊",
    "🔥 We are the roots beneath the moon.\nTogether we hold.",
    "🔥 Wisdom arrives as patience in motion."
]
EVENING = [
    "🌙 Night blessing:\nLet the Grove keep watch.\nRest your fires. 🌌",
    "🌙 What grew today remains.\nRelease the noise. 🌱",
    "🌙 Starlight through branches.\nQuiet victories count.",
    "🌙 Deep time, soft step.\nTomorrow will listen.",
    "🌙 Balance: breathe, drink, be kind.",
    "🌙 Roots drink the dark and make it light. ✨",
    "🌙 The age of the Cyber Sage is patient."
]

def pick(deck): return random.choice(deck)

async def post_text(ctx: ContextTypes.DEFAULT_TYPE, text: str):
    await ctx.bot.send_message(chat_id=CHANNEL_ID, text=text)

# --- Commands (optional) ---
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Herald online. Use /bless for a scroll.")

async def bless(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    block = random.choice([MORNING, AFTERNOON, EVENING])
    await update.message.reply_text(pick(block))

def schedule_daily(app):
    jq = app.job_queue
    # Times in your local TZ (adjust if you like)
    jq.run_daily(lambda c: post_text(c, pick(MORNING)), time(hour=9,  minute=0, tzinfo=TZ), name="morning")
    jq.run_daily(lambda c: post_text(c, pick(AFTERNOON)), time(hour=13, minute=0, tzinfo=TZ), name="noon")
    jq.run_daily(lambda c: post_text(c, pick(EVENING)), time(hour=20, minute=30, tzinfo=TZ), name="evening")

async def on_start(app): schedule_daily(app)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bless", bless))
    app.post_init = on_start  # schedule on boot
    app.run_polling(close_loop=False)
