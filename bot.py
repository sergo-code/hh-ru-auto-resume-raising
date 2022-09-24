import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import asyncio

import os
import time
from dotenv import load_dotenv

from keyboard import home, TextButtonList
from main_async import HHru
from status_code import status


class AddResume(StatesGroup):
    title = State()
    time = State()


class DelResume(StatesGroup):
    title = State()


async def start(message: types.Message) -> None:
    if await is_admin(message.from_id):
        text = 'HeadHunter Resume\nСервис автоматического подъема резюме каждые 4 часа.'
        await message.answer(text, reply_markup=home)


async def auth(message: types.Message) -> None:
    if await is_admin(message.from_id):
        global obj
        if await obj.login():
            await message.answer('Авторизация выполнена!')
        else:
            await message.answer('Ошибка авторизации')


async def profile(message: types.Message) -> None:
    if await is_admin(message.from_id):
        text = '<b>Ваши данные</b>\n' \
               f"Телефон: {os.getenv('phone')}\n" \
               f"Пароль: {os.getenv('password')}\n" \
               f"Прокси: {os.getenv('proxy')}"
        await message.answer(text, parse_mode='html')


async def update_list_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        global obj
        if await obj.get_resumes():
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n{title}'
            await message.answer(text, parse_mode='html')
        else:
            text = 'Необходимо авторизоваться.'
            await message.answer(text, parse_mode='html')


async def list_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        global obj
        if len(obj.resume_src) > 0:
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n{title}'
        else:
            text = '<b>Резюме не найдено</b>' \
                   '\n1) Попробуйте обновить список резюме.' \
                   '\n2) Проверьте наличие резюме в профиле hh.ru'
        await message.answer(text, parse_mode='html')


async def list_active_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        global obj
        if len(obj.resume_active) > 0:
            text = '<b>Расписание</b>'
            for title, value in obj.resume_active.items():
                text += f"\n{title}"
                if value['last_raise'] == '99:99':
                    text += f"\n\nПоследние поднятие:\n<u>нет данных</u>\n"
                else:
                    text += f"\n\nПоследние поднятие:\n<u>{value['last_raise']}</u>\n"

                obj.purpose_time = int(value['time']['hour'])
                obj.choice_time()
                for hour in obj.update_time_list:
                    text += f"\n<code>{hour}:{value['time']['minute']}</code>"
                text += '\n'
        else:
            text = 'Ни одно резюме не добавлено в расписание.'
        await message.answer(text, parse_mode='html')


async def add_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        global obj
        if len(obj.resume_src) > 0:
            await AddResume.title.set()
            text = 'Введите наименование резюме, которое нужно поднимать.'
            await message.answer(text)
        else:
            text = 'Обновите список резюме.'
            await message.answer(text)


async def set_resume(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['title'] = message.text
    await AddResume.next()
    text = 'Введите время поднятия, например 14:00 будет соответствовать ' \
           '2:00 6:00 10:00 <code>14:00</code> 18:00 22:00'
    await message.answer(text, parse_mode='html')


async def set_time(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['time'] = message.text
    time_ = data['time'].split(':')
    await obj.add_resume_active(data['title'], time_[0], time_[1])
    text = f'<b>Добавлено новое расписание</b>' \
           f"\n{data['title']}" \
           f"\n{data['time']}"
    await message.answer(text, parse_mode='html')
    await state.finish()


async def del_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        if len(obj.resume_active) > 0:
            await DelResume.title.set()
            await message.answer('Введите наименование резюме, которое хотите удалить.')
        else:
            await message.answer('В расписании нет резюме')


async def set_title(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['title'] = message.text
    await obj.del_resume_active(data['title'])
    text = "<b>Удалено следующее резюме</b>" \
           f"\n{data['title']}"
    await message.answer(text, parse_mode='html')
    await state.finish()


async def is_admin(user_id: int) -> bool:
    await asyncio.sleep(0.01)
    return True if user_id == int(os.getenv('admin_tg')) else False


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
        if await obj.check_proxy():
            await obj.login()
            code = await obj.raise_resume(obj.resume_active[title]['resume_id'])
            if code == 409:
                return code
            elif code == 200:
                obj.resume_active[title]['last_raise'] = f'{now_time_hour}:{now_time_minute}'
                return code
            else:
                return 1
        else:
            return 0


async def tasks() -> None:
    global obj
    code = None
    # Проверка на ошибку авторизации (1) и прокси (0)
    while True and (code != 0 or code != 1):
        sleep_time = time.localtime(time.time())
        sleep_time_seconds = int(time.strftime("%S", sleep_time))
        await asyncio.sleep(60-sleep_time_seconds)
        # Проверяет есть ли резюме, которые нужно поднимать
        if len(obj.resume_active) > 0:
            now_time = time.localtime(time.time())
            now_time_hour = time.strftime("%H", now_time)
            now_time_minute = time.strftime("%M", now_time)
            # Проходит по каждому резюме отдельно
            for title, value in obj.resume_active.items():
                # Проверка выполнения условия по времени (раз в 4 часа)
                if (int(value['time']['hour']) - int(now_time_hour)) % 4 == 0:
                    if value['last_raise'] != '99:99' or int(value['last_raise'].split(':')[0]) != int(now_time_hour):
                        if int(now_time_minute) == int(value['time']['minute']):
                            # Алгоритм поднятия резюме
                            code = await algorithm(title, now_time_hour, now_time_minute)
                            print(status(code))
                            if code == 0 or code == 1:
                                break


async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    asyncio.create_task(tasks())


def create_bot() -> None:
    bot = Bot(token=os.getenv('bot_token'))
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(auth, text=[TextButtonList['auth']])
    dp.register_message_handler(profile, text=[TextButtonList['profile']])
    dp.register_message_handler(update_list_resume, text=[TextButtonList['update_list_resume']])
    dp.register_message_handler(list_resume, text=[TextButtonList['list_resume']])
    dp.register_message_handler(list_active_resume, text=[TextButtonList['list_active_resume']])
    dp.register_message_handler(add_resume, text=[TextButtonList['add_resume']])
    dp.register_message_handler(set_resume, state=AddResume.title)
    dp.register_message_handler(set_time, state=AddResume.time)
    dp.register_message_handler(del_resume, text=[TextButtonList['del_resume']])
    dp.register_message_handler(set_title, state=DelResume.title)
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)


load_dotenv()
with open('config/tokens.json', 'r') as file:
    data = json.load(file)

obj = HHru(os.getenv('phone'), os.getenv('password'), {'https': os.getenv('proxy')})
if data != {}:
    obj.xsrf = data['xsrf']
    obj.hhtoken = data['hhtoken']


if __name__ == '__main__':
    create_bot()
