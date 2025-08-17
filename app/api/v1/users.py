from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.functions.configs import get_config
from app.db.functions.users import get_user_refferals
from app.models.schemas.errors import ErrorResponse
from app.models.schemas.users import BaseUserInput, UserOut, UserWithdrawIn, UserWithdrawOut
from app.models.user import User
from app.services.bot.bot_auth import authenticate_user
from app.services.ton.transfer import TonServices

router = APIRouter()


@router.post("/", response_model=UserOut | ErrorResponse)
async def get_user(
    user_in: BaseUserInput,
    session: AsyncSession = Depends(get_db)
):
    init_data = user_in.init_data
    start_param = user_in.start_param
    user: dict = await authenticate_user(
        init_data=init_data,
        start_param=start_param
    )

    if user.get("success") is False:
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )
    
    user: User = user.get("user")
    
    user_out = UserOut.model_validate(user)

    user_out.ref_count = await get_user_refferals(
        session=session,
        ref_code=user.ref_code,
        is_count=True
    )

    return user_out


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

    if user.balance < config.min_withdraw:
        return ErrorResponse(
            code="insufficient_balance",
            message="Not enough balance to withdraw.",
        )

    user_ton_balance = user.balance / config.exchange_rate
    if user_ton_balance < config.min_withdraw:
        return ErrorResponse(
            code="insufficient_balance",
            message="Not enough diamond in balance.",
        )

    if not wallet:
        return ErrorResponse(
            code="invalid_wallet",
            message="Invalid wallet address provided.",
        )
    
    transfer = await TonServices.send_transaction(
        to_address=wallet,
        amount=user_ton_balance
    )

    if not transfer:
        return ErrorResponse(
            code="transfer_error",
            message="Failed to process the withdrawal transaction.",
        )

    return UserWithdrawOut(
        new_balance=user.balance
    )