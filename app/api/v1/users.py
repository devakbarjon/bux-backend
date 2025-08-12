from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.functions.configs import get_config
from app.models.schemas.errors import ErrorResponse
from app.models.schemas.users import BaseUserInput, UserOut, UserWithdrawIn, UserWithdrawOut
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user

router = APIRouter()


@router.post("/", response_model=UserOut | ErrorResponse)
async def get_user(
    user_in: BaseUserInput
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
    
    user: User = user.get("user")
    
    return UserOut.from_orm(user)


@router.post("/withdraw", response_model=UserWithdrawOut | ErrorResponse)
async def user_withdraw(
        user_in: UserWithdrawIn,
        session: AsyncSession = Depends(get_db)
):
    init_data = user_in.init_data
    wallet = user_in.wallet
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

    user_ton_balance = user.balance / config.exchange_rate
    if user_ton_balance < config.min_withdraw:
        return ErrorResponse(
            code="balance_error",
            message="Not enough diamond in balance.",
        )

    return UserWithdrawOut(
        new_balance=user.balance
    )