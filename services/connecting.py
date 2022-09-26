from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from services.main import HHru


load_dotenv()
bot = Bot(token=os.getenv('bot_token'))
dp = Dispatcher(bot, storage=MemoryStorage())

obj = HHru(os.getenv('phone'), os.getenv('password'), os.getenv('proxy'))
