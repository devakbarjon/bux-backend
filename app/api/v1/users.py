from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.functions.configs import get_config
from app.models.schemas.users import BaseUserInput, UserOut, BaseResponse, UserWithdrawIn
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user

router = APIRouter()


@router.post("/", response_model=UserOut)
async def get_user(
    user_in: BaseUserInput
):
    init_data = user_in.init_data
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))
    
    user: User = user.get("user")
    
    return UserOut(
        user_id=user.user_id,
        lang=user.lang,
        balance=user.balance,
        adv_balance=user.adv_balance
    )


@router.post("/withdraw", response_model=BaseResponse)
async def get_user(
        user_in: UserWithdrawIn,
        session: AsyncSession = Depends(get_db)
):
    init_data = user_in.init_data
    wallet = user_in.wallet
    user: dict = await authenticate_user(
        init_data=init_data
    )

    if user.get("success") is False:
        raise HTTPException(status_code=400, detail=user.get("message", "Authentication failed"))

    user: User = user.get("user")

    config = await get_config(session=session)

    user_ton_balance = user.balance / config.exchange_rate
    if user_ton_balance < config.min_withdraw:
        raise HTTPException(status_code=400, detail="Not enough diamond in balance.")

    return BaseResponse(
        success=True,
        message="Withdraw processed successfully"
    )