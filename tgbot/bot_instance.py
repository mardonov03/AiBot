from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from tgbot.core.config import settings
import orjson

session = AiohttpSession(json_loads=orjson.loads)

bot = Bot(
    token=settings.BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
