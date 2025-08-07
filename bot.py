import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import router
from middleware import SubscriptionMiddleware
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.update.middleware(SubscriptionMiddleware())

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")