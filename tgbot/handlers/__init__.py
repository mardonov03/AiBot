from aiogram import Router, F
from aiogram.filters import Command
from tgbot.handlers import start_cmd
from tgbot.handlers import agreement_handler
from tgbot.handlers import message_handler

def setup() -> Router:
    router = Router()

    router.message.register(start_cmd.handle_start, Command('start', ignore_mention=True))

    router.callback_query.register(agreement_handler.agreement_selected, F.data.startswith("agreement_"))

    router.message.register(message_handler.request_to_ai, F.chat.type == "private")
    return router