from app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.functions import generate_random_key


async def save_user(session: AsyncSession, user_id: int, username: str | None, ref: str | None, lang: str = "en"):

    if ref == "":
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