from uuid import UUID

from app.models.job import Job


class JobRepository:
    def __init__(self) -> None:
        self._store: dict[UUID, Job] = {}

    def save(self, job: Job) -> Job:
        self._store[job.id] = job
        return job

    def find_by_id(self, job_id: UUID) -> Job | None:
        return self._store.get(job_id)

    def find_all(self) -> list[Job]:
        return sorted(self._store.values(), key=lambda j: j.created_at, reverse=True)

    def count(self) -> int:
        return len(self._store)


job_repository = JobRepository()
