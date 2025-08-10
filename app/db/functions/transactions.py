from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction


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