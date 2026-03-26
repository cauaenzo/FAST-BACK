from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job


class JobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, job: Job) -> Job:
        self._session.add(job)
        await self._session.commit()
        await self._session.refresh(job)
        return job

    async def find_by_id(self, job_id: UUID) -> Job | None:
        result = await self._session.execute(select(Job).where(Job.id == str(job_id)))
        return result.scalar_one_or_none()

    async def find_all(self) -> list[Job]:
        result = await self._session.execute(select(Job).order_by(Job.created_at.desc()))
        return list(result.scalars().all())
