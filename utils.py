from yookassa import Configuration, Payment
from config import settings
import uuid
from typing import Any

def configure_yoo() -> None:
    shop_id, secret = settings.YKASSA_TOKEN.split(":", 1)
    Configuration.account_id = shop_id
    Configuration.secret_key = secret

def create_yoo_payment(amount_cents: int, description: str) -> Any:
    configure_yoo()
    idempotence_key = str(uuid.uuid4())
    return Payment.create(
        {
            "amount": {"value": f"{amount_cents / 100:.2f}", "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": "https://t.me/your_bot"},
            "capture": True,
            "description": description,
        },
        idempotence_key,
    )

def cents_to_rub(cents: int) -> str:
    return f"{cents / 100:.0f}₽"
