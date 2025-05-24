from tgbot.core.logging import logger
from aiogram.types import Message
import aiohttp


api_url = "http://127.0.0.1:8083"

async def handle_start(message: Message):
    try:
        userid = message.from_user.id
        username = message.from_user.username or "unknown"

        async with aiohttp.ClientSession() as session:
            payload = {
                "userid": userid,
                "full_name": username,
            }
            resp = await session.post(f"{api_url}/users/add-to-db", json=payload)
            data = await resp.json()
            print(data)
            await message.answer(f"Привет! Ответ от API: {data['name']}")
    except Exception as e:
        logger.error(f'[handle_start error]: {e}')
