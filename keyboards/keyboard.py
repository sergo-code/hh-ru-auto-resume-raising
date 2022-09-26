from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TextButtonList = {
    'profile': '⚙ Профиль',
    'list_resume': '📜 Список резюме',
    'list_active_resume': '📅 Расписание',
    'add_resume': '➕ Добавить или обновить',
    'del_resume': '❌ Удалить',
    'auth': '🚀️ Авторизоваться',
    'update_list_resume': '📝 Обновить список резюме',
    'notifications': '🔔 Вкл/выкл уведомления',
}

ButtonList = dict()

for key in TextButtonList.keys():
    ButtonList[key] = KeyboardButton(TextButtonList[key])


home = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(ButtonList['profile'])\
    .insert(ButtonList['notifications'])\
    .add(ButtonList['list_resume'])\
    .insert(ButtonList['list_active_resume'])\
    .add(ButtonList['add_resume'])\
    .insert(ButtonList['del_resume'])\
    .add(ButtonList['auth'])\
    .insert(ButtonList['update_list_resume'])
