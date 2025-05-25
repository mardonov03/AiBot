from aiogram import Router
from aiogram.filters import Command
from tgbot.handlers import start_cmd

def setup() -> Router:
    router = Router()

    router.message.register(start_cmd.handle_start, Command('start', ignore_mention=True))

    return router
