from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction


async def save_transaction(session: AsyncSession, user_id: int, amount: float, status: str, transaction_id: str = None, type: str = "deposit") -> Transaction:
    transaction = Transaction(user_id=user_id, amount=amount, status=status, transaction_id=transaction_id, type=type)
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


async def get_transaction_by_id(session: AsyncSession, transaction_id: str) -> Transaction | None:
    result = await session.execute(
        select(Transaction).where(Transaction.transaction_id == transaction_id)
    )
    return result.scalars().first()


async def get_transactions_by_user(session: AsyncSession, user_id: int) -> list[Transaction]:
    result = await session.execute(
        select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc())
    )
    return result.scalars().all()