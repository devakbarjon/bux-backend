from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def save_task(session: AsyncSession, user_id: int, link: str, title: str, reward: int, type: str, check_sub: bool) -> Task:
    new_task = Task(
        user_id=user_id,
        link=link,
        title=title,
        reward=reward,
        type=type,
        check_sub=check_sub
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task
    


async def get_task_by_id(session: AsyncSession, task_id: int) -> Task | None:
    result = await session.execute(
        select(Task).where(Task.id == task_id)
    )
    return result.scalars().first()


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(
        select(Task).filter_by(status=True).order_by(Task.id)
    )
    tasks = result.scalars().all()
    return tasks


async def add_user_to_task(session: AsyncSession, task_id: int, user_id: int) -> None:
    task = await get_task_by_id(session, task_id)
    if not task:
        return None

    if user_id not in task.users:
        task.users += [user_id]
        await session.commit()
        await session.refresh(task)
    return task