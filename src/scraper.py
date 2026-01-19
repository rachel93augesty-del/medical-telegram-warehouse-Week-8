from telethon import TelegramClient
from dotenv import load_dotenv
import os
from loguru import logger
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

# Load environment variables
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")

# Initialize Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

# Setup logging to file
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
logger.add(logs_dir / f"scraper_{today}.log", rotation="10 MB")

# Channels to scrape
channels = [
    'CheMed',
    'lobelia4cosmetics',
    'tikvahpharma',
    'tenamereja'
]

async def main():
    logger.info("Connecting to Telegram...")
    await client.start(phone=PHONE)
    logger.info("Telegram client started successfully.")

    for channel in channels:
        try:
            entity = await client.get_entity(channel)
            messages = await client.get_messages(entity, limit=5)  # adjust limit as needed
            logger.info(f"Fetched {len(messages)} messages from {channel}")

            # Prepare output directories
            msg_dir = Path(f"data/raw/telegram_messages/{today}")
            msg_dir.mkdir(parents=True, exist_ok=True)
            images_dir = Path(f"data/raw/images/{channel}")
            images_dir.mkdir(parents=True, exist_ok=True)

            # Save messages and download media
            msg_list = []
            for msg in messages:
                msg_data = {
                    "message_id": msg.id,
                    "date": msg.date.isoformat(),
                    "text": msg.message,
                    "views": msg.views,
                    "forwards": msg.forwards,
                    "has_media": msg.media is not None
                }
                msg_list.append(msg_data)

                # Download media if exists
                if msg.media:
                    try:
                        file_path = await client.download_media(
                            msg, file=images_dir / f"{msg.id}.jpg"
                        )
                        logger.info(f"Downloaded media for message {msg.id} in {channel}")
                    except Exception as e:
                        logger.error(f"Failed to download media for message {msg.id}: {e}")

            # Save messages JSON
            out_file = msg_dir / f"{channel}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(msg_list, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(messages)} messages to {out_file}")

        except Exception as e:
            logger.error(f"Error fetching messages from {channel}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
