import asyncio
import logging
import sys
import time
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def main():
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        logger.error("CRITICAL ERROR: BOT_TOKEN is not set in Environment Variables!")
        return

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return
    
    # Initialize bot and dispatcher
    try:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        
        logger.info("Bot is starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
