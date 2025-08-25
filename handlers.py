import logging
from openai import OpenAI, APIStatusError, APITimeoutError
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from keyboards import menu_kb, pay_kb
from config import settings
from utils import create_yoo_payment
from bot_integration import register_user_from_bot, log_message_from_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=30
)

router = Router()

class GenState(StatesGroup):
    prompt = State()

@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    try:
        # Register user in database
        user = register_user_from_bot(message.from_user)
        if user:
            logger.info(f"User {message.from_user.id} registered/updated in database")
        
        # Log the start command
        log_message_from_bot(message.from_user.id, "/start", "command")
        
        await message.answer(
            "👋 Привет! Я AI-бот, который генерирует email-рассылки.\n"
            "Нажми «Сгенерировать» чтобы начать.",
            reply_markup=menu_kb(),
        )
    except TelegramForbiddenError:
        logger.warning(f"Blocked by user {message.from_user.id}")

@router.callback_query(F.data == "generate")
async def ask_prompt(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.edit_text("Напиши тему или продукт для рассылки:")
    await state.set_state(GenState.prompt)

@router.message(GenState.prompt)
async def generate_email(message: types.Message, state: FSMContext) -> None:
    await message.chat.do("typing")
    user_prompt = message.text[:1000]
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": f"Напиши email-рассылку для: {user_prompt}"}],
            max_tokens=800,
        )
        text = response.choices[0].message.content
    except (APIStatusError, APITimeoutError):
        text = "❌ Не удалось обратиться к OpenRouter. Попробуйте позже."
    await message.answer(text, reply_markup=menu_kb())
    await state.clear()

@router.callback_query(F.data == "pay")
async def send_invoice(callback: types.CallbackQuery) -> None:
    await callback.answer()
    try:
        payment = create_yoo_payment(settings.PRICE_MONTH, "Премиум 30 дней")
    except Exception:
        await callback.message.answer("❌ Ошибка создания платежа.")
        return
    await callback.message.answer(
        f"💳 Оплата {settings.PRICE_MONTH / 100}₽ на 30 дней",
        reply_markup=pay_kb(payment.confirmation.confirmation_url),
    )