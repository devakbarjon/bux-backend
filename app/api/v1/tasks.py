from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.configs import get_config
from app.db.functions.tasks import get_all_tasks
from app.models.schemas.tasks import TaskListResponse, AddTaskIn
from app.models.schemas.users import BaseUserInput, BaseResponse
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user

router = APIRouter()


@router.post("/", response_model=TaskListResponse)
async def get_tasks(
        user_in: BaseUserInput,
        session: AsyncSession = Depends(get_db)
):
    init_data = user_in.init_data
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))

    tasks = await get_all_tasks(
        session=session
    )

    return TaskListResponse(tasks=tasks)


@router.post("/add", response_model=BaseResponse)
async def add_task(
        task_in: AddTaskIn,
        session: AsyncSession = Depends(get_db)
):
    init_data = task_in.init_data
    link = task_in.link
    check_sub = task_in.check_sub
    count = task_in.count
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))

    user: User = user.get("user")

    config = await get_config(session=session)

    task_price = count * config.task_price

    if user.balance < task_price:
        raise HTTPException(status_code=400, detail="Not enough ton in balance.")

