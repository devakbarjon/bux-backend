from app.models.user import User
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.functions import generate_random_key


async def save_user(session: AsyncSession, user_id: int, username: str | None, ref: str | None, lang: str = "en"):

    if ref == "":
        ref = None

    if ref and ref.startswith("r_"):
        ref = ref.split("_", 1)[1]
        ref_user = await session.execute(
            select(User).where(User.ref_code == ref)
        )
        ref_user = ref_user.scalars().first()
        if not ref_user:
            ref = None

    if lang not in ["en", "ru"]:
        lang = "ru"


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


async def update_user_adv_balance(session: AsyncSession, user_id: int, amount: int | float, increase: bool = True) -> User:
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


async def get_user_refferals(session: AsyncSession, ref_code, is_count: bool = False):
    query = select(User).where(User.ref == ref_code)

    if is_count:
        result = await session.execute(query.with_only_columns(func.count()))
        return result.scalar_one()
    else:
        result = await session.execute(query)
        return result.scalars().all()
    


async def reset_user_balance(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session, user_id)
    if not user:
        return None

    user.balance = 0
    await session.commit()
    await session.refresh(user)
    return user


async def complete_task_for_user(session: AsyncSession, user_id: int, task_id: int) -> User:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None

    if str(task_id) not in user.tasks_completed:
        user.tasks_completed = user.tasks_completed + [str(task_id)]
        await session.commit()
        await session.refresh(user)
    return user