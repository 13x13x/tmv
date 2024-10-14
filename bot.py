from pyrogram import Client
import requests
from bs4 import BeautifulSoup
import asyncio
import os
import uuid
import nest_asyncio
import feedparser

api_id = 24972774
api_hash = '188f227d40cdbfaa724f1f3cd059fd8b'
bot_token = '6641807680:AAFJMvQ-t6NaxIxoB2oU_ovzc73VDLVG8Gc'

session_name = f"web_scraper_bot_{api_id}_{uuid.uuid4()}"

os.makedirs("./sessions", exist_ok=True)

app = Client(
    session_name,
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    workdir="./sessions"
)

user_chat_id = 5549620776  # Your Telegram user ID

def get_rss_links(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        links = []
        for entry in feed.entries:
            if 'link' in entry:
                links.append(entry.link)
        return links
    except Exception as e:
        return []

async def send_links_or_message(links):
    if links:
        for link in links:
            formatted_link = f"**/qbleech {link}** \n**Tag:** `@Arisu_0007 5549620776`"
            await app.send_message(user_chat_id, formatted_link)
            await asyncio.sleep(1)
    else:
        await app.send_message(user_chat_id, "**Links Not Found!!**")

async def automatic_tmv():
    while True:
        feed_url = "https://rss.app/feeds/FFh0vlIMaf9K5TPJ.xml"
        links = get_rss_links(feed_url)
        await send_links_or_message(links)
        await asyncio.sleep(900)  # Wait for 900 seconds before checking again

async def main():
    await app.start()
    print("Bot started and will send RSS feed links every 900 seconds.")
    await automatic_tmv()  # Start the automatic scraping process

nest_asyncio.apply()
asyncio.run(main())
