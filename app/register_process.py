import asyncio
import multiprocessing as mp

from aiogram import Bot, Dispatcher

dispatcher_process: mp.Process = None


async def register_checker(dp: Dispatcher, bot: Bot, allowed_updates):
    await asyncio.create_task(dp.start_polling(bot, allowed_updates=allowed_updates))
