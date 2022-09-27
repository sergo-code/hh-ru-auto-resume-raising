import asyncio

from .env import Config


async def is_admin(user_id: int) -> bool:
    await asyncio.sleep(0.01)
    return True if user_id == int(Config.admin_tg) else False
