from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job:
    def __init__(self, payload: dict[str, Any], priority: int = 0) -> None:
        self.id: UUID = uuid4()
        self.payload: dict[str, Any] = payload
        self.priority: int = priority
        self.status: JobStatus = JobStatus.PENDING
        self.result: Any = None
        self.error: str | None = None
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self.started_at: datetime | None = None
        self.finished_at: datetime | None = None

    def start(self) -> None:
        self.status = JobStatus.PROCESSING
        self.started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def complete(self, result: Any = None) -> None:
        self.status = JobStatus.COMPLETED
        self.result = result
        self.finished_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error
        self.finished_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
