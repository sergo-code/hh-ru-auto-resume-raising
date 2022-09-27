import time
import os
import asyncio

from .env import Config
from .connecting import obj, bot
from .status_code import status


async def update_time(title):
    await asyncio.sleep(0.01)
    obj.resume_active[title]['time']['hour'] = (int(time.strftime('%H')) + 4) % 24
    obj.resume_active[title]['time']['minute'] = int(time.strftime('%M'))
    obj.resume_active[title]['time']['seconds'] = int(time.strftime('%S'))
    obj.resume_active[title]['ltime']['hour'] = int(time.strftime('%H'))


async def algorithm(title):
    await asyncio.sleep(0.01)
    '''
    Смотреть status_code.py для информации по коду состояния
    '''
    code = await obj.raise_resume(obj.resume_active[title]['resume_id'])
    if code == 409:
        await update_time(title)
        return code
    elif code == 200:
        await update_time(title)
        return code
    else:
        await obj.login()
        code = await obj.raise_resume(obj.resume_active[title]['resume_id'])
        if code == 409:
            await update_time(title)
            return code
        elif code == 200:
            await update_time(title)
            return code
        else:
            return code


async def tasks() -> None:
    code = None
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    # Проверка на ошибку авторизации (1) и прокси (0)
    while True and (code != 0 or code != 1):
        await asyncio.sleep(1)
        # Проверяет есть ли резюме, которые нужно поднимать
        if len(obj.resume_active) > 0:
            now_time_hour = int(time.strftime("%H"))
            now_time_minute = int(time.strftime("%M"))
            now_time_seconds = int(time.strftime("%S"))

            # Проходит по каждому резюме отдельно
            for title, value in obj.resume_active.items():
                # Проверка: если последние поднятие не равно текущему часу
                # Проверка: поднятие раз в 4 часа
                # Проверка: минуты меньше или равно текущему
                # Проверка: секунды меньше текущих
                if value['ltime']['hour'] != now_time_hour and \
                        (value['time']['hour'] - now_time_hour) % 4 == 0 and \
                        value['time']['minute'] <= now_time_minute and \
                        value['time']['seconds'] < now_time_seconds:

                    # Алгоритм поднятия резюме
                    code = await algorithm(title)
                    text = f"<b>{title}</b>\n{status(code)}\n{time.strftime('%H:%M:%S')}"
                    if obj.notifications:
                        await bot.send_message(Config.admin_tg, text, parse_mode='html')
                    if code == 0 or code == 1:
                        break
