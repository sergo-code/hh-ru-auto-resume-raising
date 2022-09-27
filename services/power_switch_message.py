from aiogram import Dispatcher
import asyncio
import time
import os

from .auto_raise_resume import tasks
from .connecting import bot
from .env import Config


async def on_startup(dispatcher: Dispatcher) -> None:
    asyncio.create_task(tasks())
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    text = '🟩 Бот включился' \
           f'\n{time.strftime("%H:%M:%S")}'
    await bot.send_message(os.getenv('admin_tg'), text)


async def on_shutdown(dispatcher: Dispatcher) -> None:
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    text = '🟥 Бот выключился' \
           f'\n{time.strftime("%H:%M:%S")}'
    await bot.send_message(os.getenv('admin_tg'), text)
