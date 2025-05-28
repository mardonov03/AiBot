from aiogram.types import Message
import aiohttp
from tgbot.core.logging import logger
from tgbot.core.config import settings

async def request_to_ai(message: Message):
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

            resp = await session.post(f'{settings.API}/ai' , json={"userid": userid, "context": message.text}, headers=headers)
            data = await resp.json()
            if data['status'] == "ok":
                await message.answer(data['response'])
            elif data['status'] == "need_agreement":
                pass
    except Exception as e:
        logger.error(f'[request_to_ai error]: {e}')