from app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.functions import generate_random_key


async def save_user(session: AsyncSession, user_id: int, username: str | None, ref: str | None, lang: str = "en"):

    if ref == "":
        ref = None

    if ref:
        ref_user = await session.execute(
            select(User).where(User.ref_code == ref)
        )
        ref_user = ref_user.scalars().first()
        if not ref_user:
            ref = None


    user = User(
        user_id=user_id,
        ref_code=await generate_random_key(length=8),
        username=username,
        ref=ref,
        lang=lang,
    )
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


async def update_user_balance(session: AsyncSession, user_id: int, amount: int, increase: bool = True) -> User:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None

    if increase:
        user.balance += amount
    else:
        user.balance -= amount
    await session.commit()
    await session.refresh(user)
    return user.balance


async def update_user_adv_balance(session: AsyncSession, user_id: int, amount: int, increase: bool = True) -> User:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None

    if increase:
        user.adv_balance += amount
    else:
        user.adv_balance -= amount
    await session.commit()
    await session.refresh(user)
    return user.adv_balance