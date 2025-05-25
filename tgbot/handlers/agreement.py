from aiogram.types import CallbackQuery
from tgbot.core.logging import logger
import aiohttp
from tgbot.core.config import settings
from tgbot.keyboards import config as keyboards


async def agreement_selected(callback_query: CallbackQuery):
    userid = callback_query.from_user.id
    selected = callback_query.data.replace('agreement_', '')
    try:
        if selected == 'yes':
            async with aiohttp.ClientSession() as session:
                res = await session.post(f'{settings.API}/agreement/update', json={'userid': userid, 'agreement_status': True})
                response_data = await res.json()
                if response_data['status'] == 'ok':
                    await callback_query.message.edit_text("<b>✅ Вы успешно подтвердили соглашение</b>.\n\n🇷🇺 Ru: <b><a href='https://telegra.ph/Polzovatelskoe-Soglashenie-PurifyAi-04-13-2'>Пользовательское Соглашение</a> </b>.\n\n🇺🇸 En: <b><a href='https://telegra.ph/User-Agreement-PurifyAi-04-13'>User Agreement</a> </b>.\n\n🇺🇿 Uz: <b><a href='https://telegra.ph/Foydalanuvchi-Shartnomasi-PurifyAi-04-13'>Foydalanuvchi Shartnomasi</a> </b>.\n\nСпасибо за согласие!",parse_mode="HTML", disable_web_page_preview=True)
                    await callback_query.message.chat.pin_message(callback_query.message.message_id)
                else:
                    await callback_query.answer("❌ Ошибка: доступ не разрешён. Повторите попытку.",show_alert=True)
        elif selected == 'no':
            await callback_query.message.edit_text("<b>❌ Вы отклонили пользовательское соглашение.</b>\n\nК сожалению, вы не можете использовать бота без согласия.",parse_mode="HTML")
            await callback_query.message.chat.pin_message(callback_query.message.message_id)
    except Exception as e:
        logger.error(f'"agreement_selected error": {e}')
        await callback_query.message.edit_text("Произошла ошибка. Попробуйте позже.", show_alert=True)