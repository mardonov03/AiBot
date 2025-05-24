from tgbot.core.logging import logger
from aiogram.types import Message

async def handle_start(message: Message) -> None:
    if message.chat.type == 'private':
        try:
            pass
        except Exception as e:
            logger.error(f'[handle_start error]: {e}')