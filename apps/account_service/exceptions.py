# exceptions.py

class UserAlreadyExistsError(ValueError):
    """Вызывается, когда пользователь с таким email или телефоном уже существует."""
    pass


class InvalidPasswordError(ValueError):
    pass


class PustoyLoginParolError(ValueError):
    pass

class ZaprosError(ValueError):
    pass


class UserNotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    """Общая ошибка валидации данных."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PostNotFoundError(ValueError):
    """Вызывается, когда пост не найден."""
    pass


class ExpiredTokenError(ValueError):
    """Вызывается, когда JWT-токен просрочен."""
    pass


class InvalidTokenError(ValueError):
    """Вызывается, когда JWT-токен повреждён или подделан."""
    pass