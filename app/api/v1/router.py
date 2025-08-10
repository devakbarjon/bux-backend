from fastapi import APIRouter
from .users import router as users_router
from .tasks import router as tasks_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])

router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])