import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import bot.middlewares as core

from bot.handlers import common
from bot.FSM import fsm_test

from db import init
from configs.settings import env_parameters
from register_process import register_checker

# logging main.py

logger = logging.getLogger(__name__)

bot = Bot(token=env_parameters.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


async def main():
    # Database initialization
    # try:
    #     await init()
    # except Exception as error:
    #     logger.error('Error in initialization DB', exc_info=error)

    # Settings for correct work of a dispatcher
    dp = Dispatcher(storage=MemoryStorage())

    # Connecting i18n
    core.i18n.setup(dp)

    # Connecting routers
    dp.include_router(common.router)
    dp.include_router(fsm_test.router)

    await register_checker(dp=dp, bot=bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
