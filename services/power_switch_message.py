from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

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
    try:
        await bot.send_message(os.getenv('admin_tg'), text)
    except ChatNotFound:
        pass
    except BotBlocked:
        print('[Запуск] Бот заблокирован пользователем')


async def on_shutdown(dispatcher: Dispatcher) -> None:
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    text = '🟥 Бот выключился' \
           f'\n{time.strftime("%H:%M:%S")}'
    try:
        await bot.send_message(os.getenv('admin_tg'), text)
    except ChatNotFound:
        pass
    except BotBlocked:
        print('[Отключение] Бот заблокирован пользователем')
