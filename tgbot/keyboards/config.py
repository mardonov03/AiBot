from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

def cancel():
    return ReplyKeyboardRemove()

def agreement_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, я согласен", callback_data="agreement_yes"),
            InlineKeyboardButton(text="❌ Нет, я не согласен", callback_data="agreement_no")
        ]
    ])