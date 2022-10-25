import time
import os
import asyncio

from .env import Config
from .connecting import obj, bot
from .status_code import status


async def update_time(title):
    await asyncio.sleep(0.01)
    _time = int(time.time())
    _time_obj = time.localtime(_time)
    obj.resume_active[title]['unixtime'] = _time + (60 * 60 * 4)
    obj.resume_active[title]['lunixtime'] = _time
    obj.resume_active[title]['time']['hour'] = (int(_time_obj.tm_hour) + 4) % 24
    obj.resume_active[title]['time']['minute'] = int(_time_obj.tm_min)
    obj.resume_active[title]['time']['seconds'] = int(_time_obj.tm_sec)


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

            # Проходит по каждому резюме отдельно
            for title, value in obj.resume_active.items():

                if time.localtime(value['lunixtime']).tm_hour != time.localtime(time.time()).tm_hour and \
                        value['unixtime'] - int(time.time()) < 0:

                    # Алгоритм поднятия резюме
                    code = await algorithm(title)
                    text = f"<b>{title}</b>\n{status(code)}\n{time.strftime('%H:%M:%S')}"
                    if obj.notifications:
                        await bot.send_message(Config.admin_tg, text, parse_mode='html')
                    if code == 0 or code == 1:
                        break
