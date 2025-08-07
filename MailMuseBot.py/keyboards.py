from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤖 Сгенерировать email", callback_data="generate")],
            [InlineKeyboardButton(text="💎 Премиум", callback_data="pay")],
        ]
    )

def pay_kb(payment_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
            [InlineKeyboardButton(text="✅ Проверить оплату", callback_data="check_pay")],
        ]
    )