from app.models.user import User
from app.models.transaction import Transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.functions import generate_random_key


# User-related database operations
async def save_user(session: AsyncSession, user_id: int, username: str | None, lang: str = "en"):
    user = User(user_id=user_id, username=username, lang=lang)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    result = await session.execute(
        select(User).where(User.user_id == user_id)
    )
    user = result.scalars().first()
    return user


# Transaction-related database operations
async def save_transaction(session: AsyncSession, user_id: int, amount: float, status: str, transaction_id: str = None):
    transaction = Transaction(user_id=user_id, amount=amount, status=status, transaction_id=transaction_id)
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction


async def update_transaction_status(session: AsyncSession, transaction_id: str, new_status: str):
    result = await session.execute(
        select(Transaction).where(Transaction.transaction_id == transaction_id)
    )
    transaction = result.scalars().first()
    
    if not transaction:
        return None
    
    transaction.status = new_status
    await session.commit()
    await session.refresh(transaction)
    return transaction