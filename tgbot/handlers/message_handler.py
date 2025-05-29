from aiogram.types import Message
import aiohttp
from tgbot.core.logging import logger
from tgbot.core.config import settings
from tgbot.handlers import agreement_handler
from tgbot.bot_instance import bot

async def request_to_ai(message: Message):
    if message.from_user.id == message.bot.id:
        return
    userid = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-User-ID": str(userid),
                "X-Username": username if username else "",
                "X-Full-Name": full_name
            }

            resp = await session.post(f'{settings.API}/ai/' , json={"userid": userid, "context": message.text}, headers=headers)
            data = await resp.json()
            if data['status'] == "ok":
                await message.answer(data['response'])
            elif data['status'] == "need_agreement":
                await agreement_handler.need_agreement_handler(userid, message)
                return
    except Exception as e:
        logger.error(f'[request_to_ai error]: {e}')


async def send_message_handler(userid, message_text):
    try:
        await bot.send_message(userid, message_text)
    except Exception as e:
        logger.error(f'[send_message_handler error]: {e}')
