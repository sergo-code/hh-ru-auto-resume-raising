from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import asyncio

import os
from dotenv import load_dotenv

from keyboard import home, TextButtonList
from main_async import HHru
from status_code import status

load_dotenv()

bot = Bot(token=os.getenv('bot_token'))
dp = Dispatcher(bot, storage=MemoryStorage())

load_dotenv()
obj = HHru(os.getenv('phone'), os.getenv('password'), {'https': os.getenv('proxy')})


class AddResume(StatesGroup):
    title = State()
    time = State()


class DelResume(StatesGroup):
    title = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await is_admin(message.from_id):
        text = 'HeadHunter Resume\nСервис автоматического подъема резюме каждые 4 часа.'
        await message.answer(text, reply_markup=home)


@dp.message_handler(text=[TextButtonList['auth']])
async def auth(message: types.Message):
    if await is_admin(message.from_id):
        global obj
        await obj.login()
        await message.answer('Выполнена авторизация!')


@dp.message_handler(text=[TextButtonList['profile']])
async def profile(message: types.Message):
    if await is_admin(message.from_id):
        text = '<b>Ваши данные</b>\n' \
               f"Телефон: {os.getenv('phone')}\n" \
               f"Пароль: {os.getenv('password')}\n" \
               f"Прокси: {os.getenv('proxy')}"
        await message.answer(text, parse_mode='html')


@dp.message_handler(text=[TextButtonList['list_resume']])
async def list_resume(message: types.Message):
    if await is_admin(message.from_id):
        global obj
        await obj.get_resumes()
        text = '<b>Ваши резюме</b>'
        for title in obj.resume_src.keys():
            text += f'\n{title}'
        await message.answer(text, parse_mode='html')


@dp.message_handler(text=[TextButtonList['list_active_resume']])
async def list_resume(message: types.Message):
    if await is_admin(message.from_id):
        global obj
        await obj.get_resumes()
        text = '<b>Ваши резюме</b>'
        for title, value in obj.resume_active.items():
            text += f"\n{title} - {value['time']}:00"
        await message.answer(text, parse_mode='html')


@dp.message_handler(text=[TextButtonList['add_resume']])
async def add_resume(message: types.Message):
    if await is_admin(message.from_id):
        await AddResume.title.set()
        await message.answer('Введите наименование резюме, которое нужно поднимать.')


@dp.message_handler(state=AddResume.title)
async def set_resume(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await AddResume.next()
    await message.answer('Выберете время поднятия, например 14:00, тогда введите число 14 (действующие от 0 до 23)')


@dp.message_handler(state=AddResume.time)
async def set_proxy(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await obj.add_resume_active(data['title'], data['time'])
    text = f'<b>Добавлено новое резюме</b>' \
           f"\n{data['title']}" \
           f"\n{data['time']}:00"
    await message.answer(text, parse_mode='html')
    await state.finish()


@dp.message_handler(text=[TextButtonList['del_resume']])
async def del_resume(message: types.Message):
    await DelResume.title.set()
    await message.answer('Введите наименование резюме, которое хотите удалить.')


@dp.message_handler(state=DelResume.title)
async def set_resume(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await obj.del_resume_active(data['title'])
    text = "<b>Удалено следующее резюме</b>" \
           f"\n{data['title']}"
    await message.answer(text, parse_mode='html')
    await state.finish()


async def is_admin(user_id: int):
    await asyncio.sleep(0.01)
    return True if user_id == int(os.getenv('admin_tg')) else False


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # asyncio.run(func())
