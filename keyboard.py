from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TextButtonList = {
    'profile': '⚙️ Профиль',
    'auth': '⚙️ Авторизоваться',
    'list_resume': '📜 Список резюме',
    'list_active_resume': '📜 Список активных резюме',
    'add_resume': '➕ Добавить резюме в расписание',
    'del_resume': '❌ Удалить резюме из расписания',
}

ButtonList = dict()

for key in TextButtonList.keys():
    ButtonList[key] = KeyboardButton(TextButtonList[key])


home = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(ButtonList['profile'])\
    .insert(ButtonList['auth'])\
    .add(ButtonList['list_resume'])\
    .insert(ButtonList['list_active_resume'])\
    .add(ButtonList['add_resume'])\
    .insert(ButtonList['del_resume'])
