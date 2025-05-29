from aiogram.types import Message
from tgbot.keyboards import config as keyboards
from aiogram.types import CallbackQuery
from tgbot.core.logging import logger
import aiohttp
from tgbot.core.config import settings

async def agreement_selected(callback_query: CallbackQuery):
    userid = callback_query.from_user.id
    selected = callback_query.data.replace('agreement_', '')
    try:
        async with aiohttp.ClientSession() as session:
            if selected == 'yes':
                res = await session.post(f'{settings.API}/agreement/update', json={'userid': userid, 'status': True})
                response_data = await res.json()
                if response_data['status'] == 'ok':
                    await callback_query.message.edit_text(f"<b>✅ Вы успешно подтвердили соглашение</b>.\n\n🇷🇺 Ru: <b><a href='{settings.AGREEMENT_URL_RU}'>Пользовательское Соглашение</a> </b>.\n\n🇺🇸 En: <b><a href='{settings.AGREEMENT_URL_EN}'>User Agreement</a> </b>.\n\n🇺🇿 Uz: <b><a href='{settings.AGREEMENT_URL_UZ}'>Foydalanuvchi Shartnomasi</a> </b>.\n\nСпасибо за согласие!",parse_mode="HTML", disable_web_page_preview=True)
                    await callback_query.message.chat.pin_message(callback_query.message.message_id)
                else:
                    await callback_query.answer("❌ Ошибка: доступ не разрешён. Повторите попытку.",show_alert=True)
            elif selected == 'no':
                res = await session.post(f'{settings.API}/agreement/update', json={'userid': userid, 'status': False})
                response_data = await res.json()
                if response_data['status'] == 'ok':
                    await callback_query.message.edit_text("<b>❌ Вы отклонили пользовательское соглашение.</b>\n\nК сожалению, вы не можете использовать бота без согласия.",parse_mode="HTML")
                    await callback_query.message.chat.pin_message(callback_query.message.message_id)
    except Exception as e:
        logger.error(f'"agreement_selected error": {e}')
        await callback_query.message.edit_text("Произошла ошибка. Попробуйте позже.", show_alert=True)

async def need_agreement_handler(userid: int, message: Message):
    await delete_agreement_message(userid, message)
    async with aiohttp.ClientSession() as session:
        mes = await message.bot.send_message(
            message.from_user.id,
            "<b>📜 Пользовательское соглашение</b>\n\nПеред использованием бота, пожалуйста, ознакомьтесь с нашим\n\n"
            "🇷🇺 Ru: <b><a href='https://telegra.ph/Polzovatelskoe-Soglashenie-PurifyAi-04-13-2'>Пользовательское Соглашение</a></b>.\n\n"
            "🇺🇸 En: <b><a href='https://telegra.ph/User-Agreement-PurifyAi-04-13'>User Agreement</a></b>.\n\n"
            "🇺🇿 Uz: <b><a href='https://telegra.ph/Foydalanuvchi-Shartnomasi-PurifyAi-04-13'>Foydalanuvchi Shartnomasi</a></b>.\n\n"
            "Вы согласны с условиями?",
            reply_markup=keyboards.agreement_keyboard(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        await session.post(f'{settings.API}/agreement/update-mesid', json={'userid': userid, 'mesid': mes.message_id})

async def delete_agreement_message(userid: int, message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(f'{settings.API}/agreement/get-mesid', params={'userid': userid})
            data = await resp.json()
            if data:
                await message.bot.delete_message(userid, data)
    except Exception as e:
        logger.info(f'[handle_start info] (trying to delete old message) {e}')
