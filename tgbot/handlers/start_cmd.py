from tgbot.core.logging import logger
from aiogram.types import Message
import aiohttp
from tgbot.core.config import settings
from tgbot.keyboards import config as keyboards

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
            if data.get('agreement_status') == 'need_agreement':
                try:
                    resp = await session.get(f'{settings.API}/agreement/get-mesid', params={'userid': userid})
                    data = await resp.json()
                    if data:
                        await message.bot.delete_message(userid, data)
                except Exception as e:
                    logger.info(f'[handle_start info] (trying to delete old message) {e}')

                mes = await message.bot.send_message(message.from_user.id, "<b>📜 Пользовательское соглашение</b>\n\nПеред использованием бота, пожалуйста, ознакомьтесь с нашим\n\n🇷🇺 Ru: <b><a href='https://telegra.ph/Polzovatelskoe-Soglashenie-PurifyAi-04-13-2'>Пользовательское Соглашение</a> </b>.\n\n🇺🇸 En: <b><a href='https://telegra.ph/User-Agreement-PurifyAi-04-13'>User Agreement</a> </b>.\n\n🇺🇿 Uz: <b><a href='https://telegra.ph/Foydalanuvchi-Shartnomasi-PurifyAi-04-13'>Foydalanuvchi Shartnomasi</a> </b>.\n\nВы согласны с условиями?", reply_markup=keyboards.agreement_keyboard(), parse_mode="HTML", disable_web_page_preview=True)
                await session.post(f'{settings.API}/agreement/update-mesid', json={'userid': userid, 'mesid': mes.message_id})
                return

            await message.answer('ok')

    except Exception as e:
        logger.error(f'[handle_start error]: {e}')