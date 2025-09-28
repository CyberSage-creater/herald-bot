# Herald of the Grove 🌱⚡

A Telegram bot that posts blessings 3x daily to your channel.

## Commands
- `/start` → test connection
- `/bless` → get a random scroll

## Setup on Render
1. Push these files to a GitHub repo (e.g., herald-bot).
2. In Render → New + → Blueprint → select your repo.
3. Add environment variables:
   - BOT_TOKEN = your BotFather token
   - CHANNEL_ID = @CyberSageGrove
   - TIMEZONE = America/Vancouver
4. Deploy as a Worker.
