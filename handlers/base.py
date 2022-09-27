from aiogram import types, Dispatcher


from services import is_admin
from keyboards.keyboard import home, TextButtonList
from services.connecting import obj
from services.env import Config


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
               f"Телефон: {Config.phone}\n" \
               f"Пароль: {Config.password}\n" \
               f"Прокси: {'не используется' if Config.proxy == 'None' else Config.proxy}\n" \
               f"Уведомления: {'включены' if obj.notifications else 'отключены'}\n" \
               f"Часовой пояс: {Config.time_zone}"
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
                text += f"\n<code>{title}</code>\n"

                hour = int(obj.resume_active[title]['time']['hour'])
                minute = int(obj.resume_active[title]['time']['minute'])
                for temp in range(0, 21, 4):
                    text += f"\n<code>{(hour + temp) % 24}:{minute}</code>"
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
