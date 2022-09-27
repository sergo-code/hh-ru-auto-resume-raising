from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from services import is_admin
from services.connecting import obj
from keyboards.keyboard import TextButtonList


class AddResume(StatesGroup):
    title = State()
    time = State()


async def add_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
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
    if data['title'] in obj.resume_src.keys():
        await AddResume.next()
        text = 'Введите время поднятия, например 14:00 будет соответствовать ' \
               '2:00 6:00 10:00 <code>14:00</code> 18:00 22:00'
        await message.answer(text, parse_mode='html')
    else:
        text = 'Резюме с таким наименованием не найдено.'
        await state.finish()
        await message.answer(text)


async def set_time(message: types.Message, state=FSMContext) -> None:
    async with state.proxy() as data:
        data['time'] = message.text
    if ':' in data['time']:
        lenght = data['time'].split(':')
        hour = lenght[0]
        minute = lenght[1]
        if hour.isnumeric() and minute.isnumeric() and len(lenght) == 2:
            if (0 <= int(hour) < 24) and (0 <= int(minute) < 60):
                await obj.add_resume_active(data['title'], int(hour), int(minute))
                text = f'<b>Добавлено новое расписание</b>' \
                       f"\n{data['title']}" \
                       f"\n{data['time']}"
            else:
                text = 'Ошибка при вводе времени, используйте формат 10:30.'
        else:
            text = 'Ошибка при вводе времени, используйте формат 10:30.'
    else:
        text = 'Ошибка при вводе времени, используйте формат 10:30.'

    await message.answer(text, parse_mode='html')
    await state.finish()


def register_handler_add_to_schedule(dp: Dispatcher):
    dp.register_message_handler(add_resume, text=[TextButtonList['add_resume']])
    dp.register_message_handler(set_resume, state=AddResume.title)
    dp.register_message_handler(set_time, state=AddResume.time)
