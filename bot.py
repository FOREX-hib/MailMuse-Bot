import asyncio, logging
from aiogram import Bot, Dispatcher
from handlers import router
from middleware import SubscriptionMiddleware
from config import settings
from app import create_app
from extensions import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.update.middleware(SubscriptionMiddleware())

# Initialize Flask app and database
flask_app = create_app()

async def main() -> None:
    # Ensure database is ready
    with flask_app.app_context():
        db.create_all()
        logging.info("Database initialized for bot")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")