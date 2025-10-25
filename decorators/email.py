import re
from functools import wraps
from fastapi import HTTPException


def validate_email(func):
    """
    Валидация email
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        email = kwargs.get('email')
        if email is None:
            raise HTTPException(status_code=400, detail="Email parameter is required")

        # Базовое регулярное выражение для email (RFC 5322 — упрощённая версия)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(email_pattern, email):
            raise HTTPException(
                status_code=400,
                detail="Invalid email format."
            )

        return await func(*args, **kwargs)

    return wrapper
