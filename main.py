# ============================================================
# Main Entry Point — School ERP Telegram Bot
# ============================================================

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import get_settings
from middlewares.auth import AuthMiddleware
from middlewares.throttling import ThrottlingMiddleware
from handlers import get_main_router


async def main():
    """Main bot entry point."""
    # Load environment variables
    load_dotenv()
    settings = get_settings()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot...")

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register Middlewares
    dp.message.middleware(ThrottlingMiddleware(rate_limit=settings.rate_limit_seconds))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=settings.rate_limit_seconds))
    
    dp.update.outer_middleware(AuthMiddleware())

    # Register Handlers
    dp.include_router(get_main_router())

    # Start polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot is polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped manually.")
