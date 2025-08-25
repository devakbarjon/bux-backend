from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.configs import get_config
from app.db.functions.tasks import add_opened_user_to_task, add_user_to_task, get_all_tasks, save_task, get_task_by_id
from app.db.functions.users import update_user_adv_balance, update_user_balance
from app.models.schemas.tasks import AddTaskOut, TaskListResponse, AddTaskIn, TaskInput, CheckTaskOut
from app.models.schemas.errors import ErrorResponse
from app.models.schemas.users import BaseUserInput, BaseResponse
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user
from app.services.bot.bot_check_sub import check_is_bot_admin
from app.utils.functions import classify_telegram_link

router = APIRouter()


@router.post("/", response_model=TaskListResponse | ErrorResponse)
async def get_tasks(
        user_in: BaseUserInput,
        session: AsyncSession = Depends(get_db)
):
    init_data = user_in.init_data
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )

    tasks = await get_all_tasks(
        session=session
    )

    return TaskListResponse(tasks=tasks)


@router.post("/add", response_model=AddTaskOut | ErrorResponse)
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
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )

    user: User = user.get("user")

    config = await get_config(session=session)

    task_price = count * config.task_price

    if user.adv_balance < task_price:
        return ErrorResponse(
            code="insufficient_balance",
            message="You do not have enough balance to add this task."
        )

    if not link.startswith("https://"):
        return ErrorResponse(
            code="invalid_link",
            message="The provided link is invalid. It must start with 'https://'."
        )
    
    link_type = await classify_telegram_link(link=link)

    if link_type == "not_telegram":
        return ErrorResponse(
            code="invalid_telegram_link",
            message="The provided link is not a valid Telegram link."
        )
    
    if check_sub and link_type != "channel":
        return ErrorResponse(
            code="invalid_link_type",
            message="Subscription check is only allowed for Telegram channels."
        )
    
    if check_sub and link_type == "channel":
        is_bot_admin = await check_is_bot_admin(channel_link=link)
        if not is_bot_admin:
            return ErrorResponse(
                code="bot_not_admin",
                message="The bot is not an admin in the specified channel."
            )
        
    new_adv_balance = await update_user_adv_balance(
        session=session,
        user_id=user.user_id,
        amount=task_price,
        increase=False
    )
        

    task = await save_task(
        session=session,
        user_id=user.user_id,
        link=link,
        title="default",
        reward=config.task_price - int(config.task_price / 100 * 40) * config.exchange_rate, # 60% of the task price * exchange rate
        type=link_type,
        check_sub=check_sub
    )

    return AddTaskOut(
        message="Task added successfully",
        new_adv_balance=new_adv_balance,
        task_id=task.id
    )


@router.post("/open", response_model=BaseResponse | ErrorResponse)
async def open_task(
        task_in: TaskInput,
        session: AsyncSession = Depends(get_db)
):
    init_data = task_in.init_data
    task_id = task_in.task_id
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )

    user: User = user.get("user")

    task = await get_task_by_id(
        session=session,
        task_id=task_id
    )

    if not task:
        return ErrorResponse(
            code="task_not_found",
            message="The requested task does not exist."
        )
    
    if user.user_id in task.users:
        return ErrorResponse(
            code="task_already_completed",
            message="You have already completed this task."
        )
    
    await add_opened_user_to_task(
        session=session,
        task_id=task.id,
        user_id=user.user_id
    )
    
    return BaseResponse(
        message="Task opened."
    )


@router.post("/check", response_model=CheckTaskOut | ErrorResponse)
async def check_task(
        task_in: TaskInput,
        session: AsyncSession = Depends(get_db)
):
    init_data = task_in.init_data
    task_id = task_in.task_id
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )

    user: User = user.get("user")

    task = await get_task_by_id(
        session=session,
        task_id=task_id
    )

    if not task:
        return ErrorResponse(
            code="task_not_found",
            message="The requested task does not exist."
        )
    
    if user.user_id in task.users:
        return ErrorResponse(
            code="task_already_completed",
            message="You have already completed this task."
        )
    
    new_balance = await update_user_balance(
        session=session,
        user_id=user.user_id,
        amount=task.reward
    )

    await add_user_to_task(
        session=session,
        task_id=task.id,
        user_id=user.user_id
    )

    return CheckTaskOut(
        message="Task completed successfully",
        task_id=task.id,
        new_balance=new_balance
    )