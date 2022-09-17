from fastapi import FastAPI

from . import api


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация',
    },
    {
        'name': 'operations',
        'description': 'Создание, редактирование, удаление и просмотр операций',
    },
]

app = FastAPI(
    title='HeadHunter',
    description='Сервис автоматического подъема резюме по расписанию',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)
