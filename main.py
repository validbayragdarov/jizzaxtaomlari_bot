import asyncio
import logging

from aiogram import Bot, Dispatcher

from db.db_control import create_userdata, create_menu, create_workers
from middlewares.antiflood import AntiFloodMiddleware

create_userdata()
create_menu()
from handlers import user_handlers, menu_handlers, basket_handlers, about_us
from admin import admin_handlers, workers_handlers
from config import TOKEN

dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN)
    dp.callback_query.middleware(AntiFloodMiddleware(0.5))
    logging.basicConfig(level=logging.INFO)
    dp.include_router(admin_handlers.router)
    dp.include_router(workers_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(menu_handlers.router)
    dp.include_router(basket_handlers.router)
    dp.include_router(about_us.router)

    await dp.start_polling(bot)


asyncio.run(main())
