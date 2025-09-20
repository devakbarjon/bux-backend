from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.functions.transactions import get_transactions_by_user
from app.models.schemas.transactions import TransListResponse, TransIn
from app.models.schemas.errors import ErrorResponse
from app.services.bot.bot_auth import authenticate_user

router = APIRouter()


@router.post("/", response_model=TransListResponse | ErrorResponse)
async def get_transactions(
        TransIn: TransIn,
        session: AsyncSession = Depends(get_db)
):
    user: dict = await authenticate_user(
        init_data=TransIn.init_data
    )

    if user.get("success") is False:
        return ErrorResponse(
            code="auth_error",
            message=user.get("message", "Authentication failed"),
        )

    user = user.get("user")

    transactions = await get_transactions_by_user(
        session=session,
        user_id=user.user_id
    )

    if not transactions:
        return TransListResponse(transactions=[])

    return TransListResponse(transactions=transactions)