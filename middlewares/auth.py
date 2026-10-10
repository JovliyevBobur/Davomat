# ============================================================
# Auth Middleware — Injects teacher data into handler context
# ============================================================

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from services.teacher_service import TeacherService
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """
    Middleware that checks if the Telegram user is a registered teacher.
    Injects 'teacher' dict into handler data if found.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Extract user from event
        user = None
        if isinstance(event, Message) and event.from_user:
            user = event.from_user
        elif isinstance(event, CallbackQuery) and event.from_user:
            user = event.from_user

        if user:
            # Look up teacher by Telegram ID
            teacher = TeacherService.get_by_telegram_id(user.id)
            data["teacher"] = teacher
            data["telegram_user"] = user
        else:
            data["teacher"] = None
            data["telegram_user"] = None

        return await handler(event, data)
