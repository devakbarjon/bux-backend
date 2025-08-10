from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def save_task(session: AsyncSession, user_id: int, prizes: str):
    giveaway = Task(id=random_id, user_id=user_id, prizes=prizes)
    session.add(giveaway)
    await session.commit()
    await session.refresh(giveaway)
    return giveaway


# async def get_giveaway_by_id(session: AsyncSession, giveaway_id: str) -> Giveaway:
#     result = await session.execute(
#         select(Giveaway).where(Giveaway.id == giveaway_id)
#     )
#     giveaway = result.scalars().first()
#     return giveaway


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(
        select(Task).order_by(Task.id)
    )
    tasks = result.scalars().all()
    return tasks
#
#
# async def update_giveaway_prizes(session: AsyncSession, giveaway_id: str, new_prizes: str):
#     result = await session.execute(
#         select(Giveaway).where(Giveaway.id == giveaway_id)
#     )
#     giveaway = result.scalars().first()
#
#     if not giveaway:
#         return None
#
#     giveaway.prizes = new_prizes
#     await session.commit()
#     await session.refresh(giveaway)
#     return giveaway
#
#
# async def update_giveaway_status(session: AsyncSession, giveaway_id: str, new_status: str):
#     result = await session.execute(
#         select(Giveaway).where(Giveaway.id == giveaway_id)
#     )
#     giveaway = result.scalars().first()
#
#     if not giveaway:
#         return None
#
#     giveaway.status = new_status
#     await session.commit()
#     await session.refresh(giveaway)
#     return giveaway