import asyncio
import feedparser
from pyrogram import Client
import os

# === CONFIG ===
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))  # your Telegram user ID or group ID
RSS_URL = "https://kawa.toonshub.my.id/series/the-fragrant-flower-blooms-with-dignity/rss"

# === INIT ===
app = Client("rss_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
seen_links = set()

async def check_feed():
    while True:
        feed = feedparser.parse(RSS_URL)
        for entry in feed.entries:
            if entry.link not in seen_links:
                text = f"🌸 *New Episode Alert!*\n\n*{entry.title}*\n{entry.link}"
                await app.send_message(CHAT_ID, text, parse_mode="markdown")
                seen_links.add(entry.link)
        await asyncio.sleep(600)  # 10 minutes

@app.on_message()
async def start_bot(_, message):
    await message.reply("Bot is running and will send updates when a new episode releases!")

async def main():
    await app.start()
    await check_feed()

if __name__ == "__main__":
    asyncio.run(main())
