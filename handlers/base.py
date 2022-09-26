from aiogram import types, Dispatcher


from services import is_admin
from keyboards.keyboard import home, TextButtonList
from services.connecting import obj

import os


async def start(message: types.Message) -> None:
    if await is_admin(message.from_id):
        text = 'HeadHunter Resume\nСервис автоматического подъема резюме каждые 4 часа.'
        await message.answer(text, reply_markup=home)


async def auth(message: types.Message) -> None:
    if await is_admin(message.from_id):
        if await obj.login():
            await message.answer('Авторизация выполнена!')
        else:
            await message.answer('Ошибка авторизации')


async def profile(message: types.Message) -> None:
    if await is_admin(message.from_id):
        text = '<b>Ваши данные</b>\n' \
               f"Телефон: {os.getenv('phone')}\n" \
               f"Пароль: {os.getenv('password')}\n" \
               f"Прокси: {'не используется' if os.getenv('proxy') == 'None' else os.getenv('proxy')}\n" \
               f"Уведомления: {'включены' if obj.notifications else 'отключены'}"
        await message.answer(text, parse_mode='html')


async def update_list_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        if await obj.get_resumes():
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n\n<code>{title}</code>'
            await message.answer(text, parse_mode='html')
        else:
            text = 'Необходимо авторизоваться.'
            await message.answer(text, parse_mode='html')


async def list_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        if len(obj.resume_src) > 0:
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n\n<code>{title}</code>'
        else:
            text = '<b>Резюме не найдено</b>' \
                   '\n1) Попробуйте обновить список резюме.' \
                   '\n2) Проверьте наличие резюме в профиле hh.ru'
        await message.answer(text, parse_mode='html')


async def list_active_resume(message: types.Message) -> None:
    if await is_admin(message.from_id):
        if len(obj.resume_active) > 0:
            text = '<b>Расписание</b>'
            for title, value in obj.resume_active.items():
                text += f"\n<code>{title}</code>"
                if value['last_raise'] == '99:99':
                    text += f"\n\nПоследние поднятие:\n" \
                            f"<u>нет данных</u>" \
                            f"\n\nСледующее поднятие:" \
                            f"\n<u>нет данных</u>\n"
                else:
                    hour = int(value['last_raise'].split(':')[0])
                    minute = int(value['last_raise'].split(':')[1])
                    text += f"\n\nПоследние поднятие:\n" \
                            f"<code>{value['last_raise']}</code>" \
                            f"\n\nСледующее поднятие:" \
                            f"\n<code>{(hour + 4) % 24}:{(minute) % 60} (+~1мин)\n"
        else:
            text = 'Ни одно резюме не добавлено в расписание.'
        await message.answer(text, parse_mode='html')


async def switch_notifications(message: types.Message) -> None:
    if await is_admin(message.from_id):
        obj.notifications = False if obj.notifications else True
        text = 'Включил' if obj.notifications else 'Отключил'
        await message.answer(text, parse_mode='html')


def register_handler_base(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(auth, text=[TextButtonList['auth']])
    dp.register_message_handler(profile, text=[TextButtonList['profile']])
    dp.register_message_handler(update_list_resume, text=[TextButtonList['update_list_resume']])
    dp.register_message_handler(list_resume, text=[TextButtonList['list_resume']])
    dp.register_message_handler(list_active_resume, text=[TextButtonList['list_active_resume']])
    dp.register_message_handler(switch_notifications, text=[TextButtonList['notifications']])
