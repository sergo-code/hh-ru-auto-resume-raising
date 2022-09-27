import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    phone = os.getenv('phone')
    password = os.getenv('password')
    proxy = os.getenv('proxy')
    bot_token = os.getenv('bot_token')
    admin_tg = os.getenv('admin_tg')
    time_zone = os.getenv('time_zone')
