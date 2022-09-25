from aiogram import executor

from handlers import (register_handler_base,
                      register_handler_add_to_schedule,
                      register_handler_delete_from_schedule)
from services import on_startup, on_shutdown, load_tokens_auth
from services.connecting import dp

load_tokens_auth()

register_handler_base(dp)
register_handler_add_to_schedule(dp)
register_handler_delete_from_schedule(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
