from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .main import HHru
from .env import Config


bot = Bot(token=Config.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

obj = HHru(Config.phone, Config.password, Config.proxy)
