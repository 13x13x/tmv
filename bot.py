from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
import asyncio
import os
import uuid
import nest_asyncio

# Replace with your own Telegram API credentials
api_id = 24972774  # Your API ID
api_hash = '188f227d40cdbfaa724f1f3cd059fd8b'  # Your API hash
bot_token = '6641807680:AAFJMvQ-t6NaxIxoB2oU_ovzc73VDLVG8Gc'  # Your bot token

# Define a unique session name using your user ID or a similar identifier
session_name = f"web_scraper_bot_{api_id}_{uuid.uuid4()}"  # Using UUID for uniqueness

# Create the sessions directory if it doesn't exist
os.makedirs("./sessions", exist_ok=True)

app = Client(
    session_name,  # Use the unique session name
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    workdir="./sessions"
)

# Function to scrape the webpage with filtering logic
def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract only links starting with the given patterns
            links = [a['href'] for a in soup.find_all('a', href=True)
                     if a['href'].startswith("magnet:?xt")]
            return links
        else:
            return []  # Return empty list if status code is not 200
    except Exception as e:
        print(f"Error while scraping: {e}")
        return []  # Return empty list in case of an error

# Function to send links or a message if no links found
async def send_links_or_message(chat_id, links):
    if links:
        for link in links:
            formatted_link = f"**/qbleech {link}** \n**Tag:** `@Arisu_0007 5549620776`"  # Use specified format
            await app.send_message(chat_id, formatted_link)  # Send each link as a separate message
            await asyncio.sleep(1)  # Adding a delay to prevent rate limiting
    else:
        # Send the "**Links Not Found!!**" message
        await app.send_message(chat_id, "**Links Not Found!!**")

# Telegram command to trigger scraping
@app.on_message(filters.command("tmv"))
async def tmv(client, message):
    try:
        url = message.text.split(" ", 1)[1]  # Get URL from message
        links = scrape_website(url)

        # Send links or message if no links found
        await send_links_or_message(message.chat.id, links)

    except IndexError:
        await message.reply_text("**Please provide a URL after the command, like this:** /scrape <url>")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

async def main():
    await app.start()  # Start the bot
    print("Bot is running...")
    try:
        await asyncio.Event().wait()  # Keep the bot running indefinitely
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await app.stop()  # Ensure the bot stops correctly

# Apply nest_asyncio and start the bot
nest_asyncio.apply()
asyncio.run(main())
