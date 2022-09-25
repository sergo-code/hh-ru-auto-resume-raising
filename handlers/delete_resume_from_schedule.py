from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from services import is_admin
from services.connecting import obj
from keyboards.keyboard import TextButtonList


class DelResume(StatesGroup):
    title = State()


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
    if await obj.del_resume_active(data['title']):
        text = "<b>Удалено следующее резюме</b>" \
               f"\n{data['title']}"
    else:
        text = 'Резюме с таким наименованием не найдено.'
    await message.answer(text, parse_mode='html')
    await state.finish()


def register_handler_delete_from_schedule(dp: Dispatcher):
    dp.register_message_handler(del_resume, text=[TextButtonList['del_resume']])
    dp.register_message_handler(set_title, state=DelResume.title)
