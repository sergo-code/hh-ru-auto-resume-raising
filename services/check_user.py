import asyncio
import os
from dotenv import load_dotenv


load_dotenv()


async def is_admin(user_id: int) -> bool:
    await asyncio.sleep(0.01)
    return True if user_id == int(os.getenv('admin_tg')) else False
