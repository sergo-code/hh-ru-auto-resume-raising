def status(code):
    if code == 200:
        return "Успешный запрос."
    elif code == 400:
        return "Резюме по заданому id не найдено."
    elif code == 403:
        return "Ошибка аутентификации, неверные токены."
    elif code == 409:
        return "Не прошло 4 часа с предыдущего поднятия резюме."
    elif code == 0:
        return 'Ошибка прокси, перепроверьте данные.'
    elif code == 1:
        return 'Ошибка авторизации.'
    else:
        return f"Неизвестная ошибка, код состояния {code}."
