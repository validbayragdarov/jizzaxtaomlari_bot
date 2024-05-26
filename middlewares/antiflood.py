from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from cachetools import TTLCache
from aiogram.types import CallbackQuery


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int | float = 2) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(self,
                       handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any:
        if event.from_user.id in self.limit:
            return
        else:
            self.limit[event.from_user.id] = None
        return await handler(event, data)
