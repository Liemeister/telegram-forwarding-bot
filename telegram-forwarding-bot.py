from telethon import TelegramClient, events
import logging
import asyncio
from googletrans import Translator
from telethon.errors import FloodWaitError
from telethon.tl.types import DocumentAttributeAnimated, DocumentAttributeSticker
import config  # Import the config file

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__name__)

# Initialize the client using credentials from config.py
client = TelegramClient('bot_session', config.api_id, config.api_hash).start(bot_token=config.bot_token)

# Google Translator
translator = Translator()

# Retry settings
RETRIES = 5   # Number of retry attempts
DELAY = 3     # Initial delay between retries
ALBUM_DELAY = 5  # Time to wait for all album messages (in seconds)

# Function to check if a message is a GIF
def is_gif(message):
    if message.gif:
        return True
    if message.document:
        if any(isinstance(attr, DocumentAttributeAnimated) for attr in message.document.attributes):
            return True
    return False

# Function to check if a message is a Sticker
def is_sticker(message):
    if message.sticker:
        return True
    if message.document:
        if any(isinstance(attr, DocumentAttributeSticker) for attr in message.document.attributes):
            return True
    return False

# Dictionary to store album messages
album_dict = {}
album_lock = asyncio.Lock()

# Handler for new messages
@client.on(events.NewMessage(chats=config.source_group))
async def message_handler(event):
    message = event.message

    if message.grouped_id:
        # This message is part of an album
        grouped_id = message.grouped_id

        async with album_lock:
            if grouped_id not in album_dict:
                album_dict[grouped_id] = []
                # Schedule processing after a delay
                asyncio.create_task(process_album_after_delay(grouped_id, ALBUM_DELAY))

            album_dict[grouped_id].append(message)

    else:
        # Only handle messages that are photos or videos, excluding GIFs and stickers
        if not (message.photo or message.video):
            return
        if is_gif(message) or is_sticker(message):
            return

        await forward_message(message)

async def process_album_after_delay(grouped_id, delay):
    await asyncio.sleep(delay)
    async with album_lock:
        messages = album_dict.pop(grouped_id, [])

    # Filter only photo or video media items, excluding GIFs and stickers
    media_messages = [
        msg for msg in messages
        if (msg.photo or msg.video) and not is_gif(msg) and not is_sticker(msg)
    ]

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

    target_groups = [config.target_group_1, config.target_group_2]

    for target_group in target_groups:
        attempt = 0
        success = False
        delay_between_retries = DELAY
        while attempt < RETRIES and not success:
            try:
                await client.send_file(target_group, media_group, caption=translated_text)
                logger.info(f"Album forwarded to {target_group}")
                success = True
            except FloodWaitError as e:
                logger.warning(f"Flood wait for {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                attempt += 1
            except Exception as e:
                logger.error(f"Error forwarding album to {target_group}, attempt {attempt + 1}: {e}")
                if attempt < RETRIES - 1:
                    await asyncio.sleep(delay_between_retries)
                    delay_between_retries += 1
                attempt += 1
        if not success:
            logger.error(f"Failed to forward album to {target_group} after {RETRIES} attempts.")

async def forward_message(message):
    if is_sticker(message):
        return  # Do not process stickers

    try:
        translated_text = translator.translate(message.text, src='auto', dest='en').text if message.text else ""
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        translated_text = message.text or ""

    target_groups = [config.target_group_1, config.target_group_2]

    for target_group in target_groups:
        attempt = 0
        success = False
        delay_between_retries = DELAY
        while attempt < RETRIES and not success:
            try:
                await client.send_message(target_group, translated_text, file=message.media)
                logger.info(f"Message forwarded to {target_group}")
                success = True
            except FloodWaitError as e:
                logger.warning(f"Flood wait for {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                attempt += 1
            except Exception as e:
                logger.error(f"Error forwarding message to {target_group}, attempt {attempt + 1}: {e}")
                if attempt < RETRIES - 1:
                    await asyncio.sleep(delay_between_retries)
                    delay_between_retries += 1
                attempt += 1
        if not success:
            logger.error(f"Failed to forward message to {target_group} after {RETRIES} attempts.")

# Start the bot
print("Bot is running...")

# Run the client
client.run_until_disconnected()
