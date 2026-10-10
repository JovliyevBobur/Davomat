# ============================================================
# Throttling Middleware — Rate limiting per user
# ============================================================

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from cachetools import TTLCache
from config import get_settings
import logging

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple rate-limiting middleware using an in-memory TTL cache.
    Prevents spam by ignoring rapid-fire messages from the same user.
    """

    def __init__(self, rate_limit: float = 1.0):
        super().__init__()
        self.rate_limit = rate_limit
        # Cache: user_id → True, expires after rate_limit seconds
        self._cache: TTLCache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if isinstance(event, Message) and event.from_user:
            user = event.from_user
        elif isinstance(event, CallbackQuery) and event.from_user:
            user = event.from_user

        if user:
            user_id = user.id
            if user_id in self._cache:
                # Rate limited — silently ignore
                if isinstance(event, CallbackQuery):
                    await event.answer("⏱ Biroz kuting...", show_alert=False)
                return
            self._cache[user_id] = True

        return await handler(event, data)
