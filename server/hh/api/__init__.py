from fastapi import APIRouter

from . import (
    auth,
    profile_hh,
    tasks,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(profile_hh.router)
router.include_router(tasks.router)

