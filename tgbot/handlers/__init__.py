from aiogram import Router, F
from aiogram.filters import Command
from tgbot.handlers import start_cmd
from tgbot.handlers import agreement

def setup() -> Router:
    router = Router()

    router.message.register(start_cmd.handle_start, Command('start', ignore_mention=True))

    router.callback_query.register(agreement.agreement_selected, F.data.startswith("agreement_"))

    return router
