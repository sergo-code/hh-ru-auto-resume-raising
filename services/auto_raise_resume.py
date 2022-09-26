import time
import os
import asyncio
from dotenv import load_dotenv

from services.connecting import obj, bot
from .status_code import status


async def algorithm(title, now_time_hour, now_time_minute):
    await asyncio.sleep(0.01)
    '''
    Смотреть status_code.py для информации по коду состояния
    '''
    code = await obj.raise_resume(obj.resume_active[title]['resume_id'])
    if code == 409:
        return code
    elif code == 200:
        obj.resume_active[title]['last_raise'] = f'{now_time_hour}:{now_time_minute}'
        return code
    else:
        await obj.login()
        code = await obj.raise_resume(obj.resume_active[title]['resume_id'])
        if code == 409:
            return code
        elif code == 200:
            obj.resume_active[title]['last_raise'] = f'{now_time_hour}:{now_time_minute}'
            return code
        else:
            return code


async def tasks() -> None:
    load_dotenv()
    code = None
    os.environ['TZ'] = os.getenv('time_zone')
    time.tzset()
    # Проверка на ошибку авторизации (1) и прокси (0)
    while True and (code != 0 or code != 1):
        sleep_time_seconds = int(time.strftime("%S"))
        await asyncio.sleep(60 - sleep_time_seconds)
        # Проверяет есть ли резюме, которые нужно поднимать
        if len(obj.resume_active) > 0:
            now_time_hour = time.strftime("%H")
            now_time_minute = time.strftime("%M")
            # Проходит по каждому резюме отдельно
            for title, value in obj.resume_active.items():
                # Проверка выполнения условия по времени (раз в 4 часа)
                if (int(value['time']['hour']) - int(now_time_hour)) % 4 == 0:
                    # Проверка условий: если последние поднятие не равно текущему часу
                    if int(value['last_raise'].split(':')[0]) != int(now_time_hour):
                        if int(now_time_minute) == 1 + int(value['time']['minute']):
                            # Алгоритм поднятия резюме
                            code = await algorithm(title, now_time_hour, now_time_minute)
                            text = f"{status(code)}\n{time.strftime('%H:%M:%S')}"
                            if obj.notifications:
                                await bot.send_message(os.getenv('admin_tg'), text)
                            if code == 0 or code == 1:
                                break
