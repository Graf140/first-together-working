import re
from functools import wraps
from fastapi import HTTPException


def validate_phone(func):
    """
    Валидация телефона, все просто
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        phone = kwargs.get('phone')
        if phone is None:
            # Если параметр не передан — ошибка (должен быть в маршруте)
            raise HTTPException(status_code=400, detail="Phone parameter is required")

        # Простая регулярка: допускаем +, цифры, пробелы, скобки, дефисы
        if not re.match(r'^[\+\d\(\)\s\-]{7,15}$', phone):
            raise HTTPException(
                status_code=400,
                detail="Invalid phone format. Use only digits, +, -, (), and spaces."
            )

        # Проверим, что есть хотя бы 7 цифр (минимальный разумный номер)
        digit_count = len(re.sub(r'\D', '', phone))
        if digit_count < 7:
            raise HTTPException(
                status_code=400,
                detail="Phone number must contain at least 7 digits."
            )

        return await func(*args, **kwargs)

    return wrapper
