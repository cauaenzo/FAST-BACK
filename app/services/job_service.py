from typing import Any
from uuid import UUID

from fastapi import HTTPException

from app.core.logging import get_logger
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate

logger = get_logger(__name__)


class JobService:
    def __init__(self, repository: JobRepository) -> None:
        self._repo = repository

    def create(self, data: JobCreate) -> Job:
        job = Job(payload=data.payload, priority=data.priority)
        self._repo.save(job)
        logger.info(f"Job criado | id={job.id} | priority={job.priority}")
        return job

    def get_by_id(self, job_id: UUID) -> Job:
        job = self._repo.find_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} não encontrado")
        return job

    def list_all(self) -> tuple[int, list[Job]]:
        jobs = self._repo.find_all()
        return len(jobs), jobs

    def update_result(self, job_id: UUID, result: Any) -> None:
        job = self._repo.find_by_id(job_id)
        if job:
            job.complete(result)
            self._repo.save(job)

    def update_failure(self, job_id: UUID, error: str) -> None:
        job = self._repo.find_by_id(job_id)
        if job:
            job.fail(error)
            self._repo.save(job)

    def mark_processing(self, job_id: UUID) -> None:
        job = self._repo.find_by_id(job_id)
        if job:
            job.start()
            self._repo.save(job)
