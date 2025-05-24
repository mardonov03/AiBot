from aiogram import Router
from aiogram.filters import Command
from tgbot.handlers import config

def setup() -> Router:
    router = Router()

    router.message.register(config.handle_start, Command('start', ignore_mention=True))

    return router
