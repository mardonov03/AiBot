import asyncio
from tgbot.core.logging import logger
import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from tgbot.core.config import settings
from tgbot import handlers
from tgbot.core import config

async def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.setup())


async def setup_middlewares(dp: Dispatcher) -> None:
    pass


async def setup_aiogram(dp: Dispatcher) -> None:
    await setup_handlers(dp)
    await setup_middlewares(dp)


async def aiogram_on_startup(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started")


async def aiogram_on_shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.session.close()
    await dispatcher.storage.close()
    logger.info("Bot shutdown")


async def main():
    session = AiohttpSession(json_loads=orjson.loads)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.startup.register(aiogram_on_startup)
    dp.shutdown.register(aiogram_on_shutdown)

    await setup_aiogram(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f'asyncio.run error: {e}')
