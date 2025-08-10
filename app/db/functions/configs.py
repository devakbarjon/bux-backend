from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.config import Config


async def get_config(session: AsyncSession) -> Config:
    result = await session.execute(
        select(Config)
    )

    config = result.scalars().first()

    return config