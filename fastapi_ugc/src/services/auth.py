import logging
from http import HTTPStatus

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError
from pydantic import ValidationError

from core.config import base_settings

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Неверный код")

        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Ошибка схемы")

        try:
            decoded_token = jwt.decode(
                credentials.credentials,
                base_settings.secret_key,
                algorithms=["HS256"],
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Истек срок действия JWT access токена"
            )
        except Exception:
            logger.exception("Ошибка проверки JWT токена")
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Неверный JWT токен")

        if not decoded_token.get("type") == "access":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Тип токена не access")

        if not self.is_authorized_account(decoded_token):
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Нет прав доступа")

        return decoded_token.get("jti")

    @staticmethod
    def is_authorized_account(decoded_token: dict) -> bool:
        try:
            return decoded_token.get("sub", {}).get("is_active")
        except ValidationError:
            logger.exception("Ошибка чтения payload JWT токена")
            return False
