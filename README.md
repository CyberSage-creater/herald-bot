
# Herald of the Grove — Telegram Bot

## What this does
- Posts 3 times daily: Morning (🍂), Afternoon (🔥), Evening (🌙)
- Rotates through 7 scrolls per deck based on weekday (Mon→#1 … Sun→#7)
- Inserts live member count automatically

## Files
- `herald_scrolls.json` — your 21 Scrolls (edit freely)
- `herald_bot.py` — the bot runner
- `requirements.txt` — libs to install
- `Procfile` — for Render/Heroku worker process

## Local run
1. Python 3.11+ recommended.
2. `pip install -r requirements.txt`
3. Export env vars:
   ```bash
   export BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   export CHAT_ID=-1001234567890   # your channel/group id
   export TIMEZONE=America/Vancouver
   export MORNING_TIME=09:00
   export AFTERNOON_TIME=13:00
   export EVENING_TIME=20:00
   ```
4. `python herald_bot.py`

## Get your CHAT_ID (easy ways)
- Add **@RawDataBot** (or **@userinfobot**) to the group/channel → say `/start` → it replies with the chat id (starts with `-100` for supergroups/channels).
- Or forward any message from your group to **@getidsbot** — it replies with the chat id.

## Deploy on Render (simple)
1. New → **Background Worker**
2. Runtime: Python 3.11+
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python herald_bot.py`
5. Environment:
   - `BOT_TOKEN` = your bot token
   - `CHAT_ID` = -100xxxxxxxxxx
   - `TIMEZONE` = America/Vancouver
   - (optional) `MORNING_TIME`, `AFTERNOON_TIME`, `EVENING_TIME`
6. Deploy. That’s it — the Herald lives.

## Customization
- Edit scroll text in `herald_scrolls.json`.
- Change post times via env vars.
- If you want a strict 7-day cycle starting a specific date, you can replace `day_index_today()` with your own function that offsets by a chosen anchor date.
