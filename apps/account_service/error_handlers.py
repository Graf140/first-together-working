#error_handlers.py

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from exceptions import *

def reg_error_handler(app):
    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request, exc):
        return HTTPException(status_code=409, detail=str(exc))

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request, exc):
        return HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(ZaprosError)
    async def zapros_handler(request, exc):
        return HTTPException(status_code=400, detail=str(exc))

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request, exc):
        return HTTPException(status_code=400, detail=str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(InvalidPasswordError)
    async def invalid_password_handler(request, exc):
        return HTTPException(status_code=401, detail=str(exc))

    @app.exception_handler(PustoyLoginParolError)
    async def empty_credentials_handler(request, exc):
        return HTTPException(status_code=400, detail=str(exc))

    @app.exception_handler(PostNotFoundError)
    async def post_not_found_handler(request, exc):
        return HTTPException(status_code=404, detail=str(exc))

    @app.exception_handler(ExpiredTokenError)
    async def expired_token_handler(request, exc):
        return HTTPException(status_code=401, detail="Token expired")

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request, exc):
        return HTTPException(status_code=401, detail="Invalid token")