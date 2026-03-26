from typing import Any
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.core.logging import get_logger
from app.models.job import Job, JobStatus
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate

logger = get_logger(__name__)


class JobService:
    def __init__(self, repository: JobRepository) -> None:
        self._repo = repository

    async def create(self, data: JobCreate) -> Job:
        job = Job(id=str(uuid4()), payload=data.payload, priority=data.priority)
        await self._repo.save(job)
        logger.info(f"Job criado | id={job.id} | priority={job.priority}")
        return job

    async def get_by_id(self, job_id: UUID) -> Job:
        job = await self._repo.find_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} não encontrado")
        return job

    async def list_all(self) -> tuple[int, list[Job]]:
        jobs = await self._repo.find_all()
        return len(jobs), jobs

    async def update_result(self, job_id: UUID, result: Any) -> None:
        job = await self._repo.find_by_id(job_id)
        if job:
            job.complete(result)
            await self._repo.save(job)

    async def update_failure(self, job_id: UUID, error: str) -> None:
        job = await self._repo.find_by_id(job_id)
        if job:
            job.fail(error)
            await self._repo.save(job)

    async def mark_processing(self, job_id: UUID) -> None:
        job = await self._repo.find_by_id(job_id)
        if job:
            job.start()
            await self._repo.save(job)
