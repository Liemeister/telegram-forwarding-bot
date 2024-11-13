from telethon import TelegramClient, events
import logging
import asyncio
from googletrans import Translator
from collections import defaultdict
from telethon.errors import FloodWaitError
from telethon.tl.types import DocumentAttributeAnimated
import config  # Import the config file

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__name__)

# Initialize the client using credentials from config.py
client = TelegramClient('bot_session', config.api_id, config.api_hash).start(bot_token=config.bot_token)

# Google Translator
translator = Translator()

# Retry settings
RETRIES = 5  # Number of retry attempts
DELAY = 3    # Initial delay between retries

# Function to check if a message is a GIF
def is_gif(message):
    if message.gif:
        return True
    if message.document:
        if any(isinstance(attr, DocumentAttributeAnimated) for attr in message.document.attributes):
            return True
    return False

# Handler for albums (grouped media messages)
@client.on(events.Album(chats=config.source_group))  # Use config.source_group
async def album_handler(event):
    # Filter only photo or video media items, excluding GIFs
    media_messages = [msg for msg in event.messages if (msg.photo or msg.video) and not is_gif(msg)]

    if not media_messages:
        return

    # Sort messages by their ID to maintain order
    media_messages.sort(key=lambda msg: msg.id)

    # Get the translated caption from the first message
    try:
        translated_text = translator.translate(media_messages[0].text, src='auto', dest='en').text if media_messages[0].text else ""
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        translated_text = media_messages[0].text or ""

    # Create a media group to send
    media_group = [msg.media for msg in media_messages]

    target_groups = [config.target_group_1, config.target_group_2]  # Use config.target_group_1, config.target_group_2

    for target_group in target_groups:
        attempt = 0
        success = False
        delay = DELAY
        while attempt < RETRIES and not success:
            try:
                # Send the media group to the target group
                await client.send_file(target_group, media_group, caption=translated_text)
                logger.info(f"Album forwarded to {target_group}")
                success = True  # Exit loop if successful
            except FloodWaitError as e:
                logger.warning(f"Flood wait for {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                attempt += 1
            except Exception as e:
                logger.error(f"Error forwarding album to {target_group}, attempt {attempt + 1}: {e}")
                if attempt < RETRIES - 1:
                    await asyncio.sleep(delay)
                    delay += 1  # Increase delay with each retry
                attempt += 1
        if not success:
            logger.error(f"Failed to forward album to {target_group} after {RETRIES} attempts.")

# Handler for standalone media messages
@client.on(events.NewMessage(chats=config.source_group))  # Use config.source_group
async def message_handler(event):
    if event.message.grouped_id:
        # This message is part of an album; it will be handled by album_handler
        return

    # Only handle messages that are photos or videos, excluding GIFs
    if not (event.message.photo or event.message.video):
        return
    if is_gif(event.message):
        return

    await forward_message(event.message)

async def forward_message(message):
    try:
        translated_text = translator.translate(message.text, src='auto', dest='en').text if message.text else ""
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        translated_text = message.text or ""

    target_groups = [config.target_group_1, config.target_group_2]  # Use config.target_group_1, config.target_group_2

    for target_group in target_groups:
        attempt = 0
        success = False
        delay = DELAY  # Use a local variable
        while attempt < RETRIES and not success:
            try:
                await client.send_message(target_group, translated_text, file=message.media)
                logger.info(f"Message forwarded to {target_group}")
                success = True  # Exit loop if successful
            except FloodWaitError as e:
                logger.warning(f"Flood wait for {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                attempt += 1
            except Exception as e:
                logger.error(f"Error forwarding message to {target_group}, attempt {attempt + 1}: {e}")
                if attempt < RETRIES - 1:
                    await asyncio.sleep(delay)
                    delay += 1  # Increase delay with each retry
                attempt += 1
        if not success:
            logger.error(f"Failed to forward message to {target_group} after {RETRIES} attempts.")

# Start the bot
print("Bot is running...")

# Run the client
client.run_until_disconnected()
