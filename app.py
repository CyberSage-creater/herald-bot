
# Herald of the Grove — Telegram Bot
# Schedules 3 daily posts (morning/afternoon/evening), rotates through 7 scrolls per deck.
# Injects live member count and appends deck signature.
#
# Env Vars:
#   BOT_TOKEN    -> Telegram bot token
#   CHAT_ID      -> Channel/group/chat id (e.g., -1001234567890)
#   TIMEZONE     -> IANA tz string (default: America/Vancouver)
#   MORNING_TIME -> HH:MM (24h) default 09:00
#   AFTERNOON_TIME -> HH:MM (24h) default 13:00
#   EVENING_TIME -> HH:MM (24h) default 20:00
#   SCROLLS_PATH -> Path to herald_scrolls.json (default: ./herald_scrolls.json)

import os
import json
import asyncio
from datetime import datetime, date
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

# --- Config ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))
TIMEZONE = os.getenv("TIMEZONE", "America/Vancouver")

MORNING_TIME = os.getenv("MORNING_TIME", "09:00")
AFTERNOON_TIME = os.getenv("AFTERNOON_TIME", "13:00")
EVENING_TIME = os.getenv("EVENING_TIME", "20:00")

SCROLLS_PATH = os.getenv("SCROLLS_PATH", "./herald_scrolls.json")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required (set env var).")
if CHAT_ID == 0:
    raise RuntimeError("CHAT_ID is required (set env var to your channel/group id).")

with open(SCROLLS_PATH, "r", encoding="utf-8") as f:
    SCROLLS = json.load(f)

TZ = ZoneInfo(TIMEZONE)
bot = Bot(token=BOT_TOKEN)

def day_index_today() -> int:
    """Return 0..6 based on local weekday (Mon=0 ... Sun=6)."""
    local_now = datetime.now(TZ)
    # Python: Monday=0, Sunday=6 — maps perfectly to 7-item decks.
    return local_now.weekday()

async def get_member_count() -> int:
    """Fetch live member count for the target chat."""
    try:
        count = await bot.get_chat_member_count(CHAT_ID)
        return int(count)
    except TelegramError as e:
        # Fallback to 0 if not available (e.g., channels may require alternative stats)
        print(f"[WARN] Failed to fetch member count: {e}")
        return 0

def render_scroll(lines: list[str], member_count: int) -> str:
    rendered = []
    for line in lines:
        rendered.append(line.replace("[X]", str(member_count)))
    return "\n".join(rendered)

async def post_deck(deck_name: str):
    idx = day_index_today()
    lines = SCROLLS[deck_name][idx]
    members = await get_member_count()
    text = render_scroll(lines, members)

    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
        print(f"[OK] Posted {deck_name} scroll #{idx+1}")
    except TelegramError as e:
        print(f"[ERROR] Failed to post {deck_name}: {e}")

async def main():
    # Immediate startup log
    me = await bot.get_me()
    print(f"Herald online as @{me.username} → posting to {CHAT_ID} in {TIMEZONE}")

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # Parse times
    m_h, m_m = map(int, MORNING_TIME.split(":"))
    a_h, a_m = map(int, AFTERNOON_TIME.split(":"))
    e_h, e_m = map(int, EVENING_TIME.split(":"))

    # Schedule daily posts
    scheduler.add_job(lambda: asyncio.create_task(post_deck("morning")),
                      CronTrigger(hour=m_h, minute=m_m))
    scheduler.add_job(lambda: asyncio.create_task(post_deck("afternoon")),
                      CronTrigger(hour=a_h, minute=a_m))
    scheduler.add_job(lambda: asyncio.create_task(post_deck("evening")),
                      CronTrigger(hour=e_h, minute=e_m))

    scheduler.start()

    # Keep running
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())
