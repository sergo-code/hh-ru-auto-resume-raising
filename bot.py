from aiogram import executor

from handlers import (register_handler_base,
                      register_handler_add_to_schedule,
                      register_handler_delete_from_schedule)
from services import on_startup, on_shutdown, load_tokens_auth, Config
from services.connecting import dp
from services.check_proxy import is_valid
from services.status_code import status


load_tokens_auth()

register_handler_base(dp)
register_handler_add_to_schedule(dp)
register_handler_delete_from_schedule(dp)


if __name__ == '__main__':
    proxy = Config.proxy
    if is_valid(proxy) or proxy == 'None':
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    else:
        print(status(0))
