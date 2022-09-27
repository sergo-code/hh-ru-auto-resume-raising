from aiogram import Dispatcher
import asyncio
import time
import os

from .auto_raise_resume import tasks
from .connecting import bot


async def on_startup(dispatcher: Dispatcher) -> None:
    asyncio.create_task(tasks())
    text = '🟩 Бот включился' \
           f'\n{time.strftime("%H:%M:%S")}'
    await bot.send_message(os.getenv('admin_tg'), text)


async def on_shutdown(dispatcher: Dispatcher) -> None:
    text = '🟥 Бот выключился' \
           f'\n{time.strftime("%H:%M:%S")}'
    await bot.send_message(os.getenv('admin_tg'), text)
