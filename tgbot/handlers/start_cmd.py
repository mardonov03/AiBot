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

        async with aiohttp.ClientSession() as session:
            resp = await session.post(f'{settings.API}/users/init-or-deny-access', json={'userid': userid, 'username': username, 'full_name': full_name})
            data = await resp.json()

            if data.get('status') == 'need_agreement':
                mes = await message.bot.send_message(message.from_user.id, "<b>📜 Пользовательское соглашение</b>\n\nПеред использованием бота, пожалуйста, ознакомьтесь с нашим\n\n🇷🇺 Ru: <b><a href='https://telegra.ph/Polzovatelskoe-Soglashenie-PurifyAi-04-13-2'>Пользовательское Соглашение</a> </b>.\n\n🇺🇸 En: <b><a href='https://telegra.ph/User-Agreement-PurifyAi-04-13'>User Agreement</a> </b>.\n\n🇺🇿 Uz: <b><a href='https://telegra.ph/Foydalanuvchi-Shartnomasi-PurifyAi-04-13'>Foydalanuvchi Shartnomasi</a> </b>.\n\nВы согласны с условиями?", reply_markup=keyboards.agreement_keyboard(), parse_mode="HTML", disable_web_page_preview=True)
                await session.post(f'{settings.API}/users/update-agreement-mesid', json={'userid': userid, 'mesid': mes.message_id})
                return

            if data.get('status') == 'ok':
                await message.answer('ok')

    except Exception as e:
        logger.error(f'[handle_start error]: {e}')