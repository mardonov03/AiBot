from tgbot.core.logging import logger
from aiogram.types import Message
import aiohttp
from tgbot.core.config import settings
from tgbot.handlers import agreement_handler


async def handle_start(message: Message):
    try:
        userid = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name

        headers = {
            "X-User-ID": str(userid),
            "X-Username": username if username else "",
            "X-Full-Name": full_name
        }

        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{settings.API}/users/get-user-data', params={'userid': userid}, headers=headers)

            data = await resp.json()
            if data.get('status') == 'need_agreement':
                await agreement_handler.need_agreement_handler(userid, message)
                return
            await message.answer('ok')

    except Exception as e:
        logger.error(f'[handle_start error]: {e}')