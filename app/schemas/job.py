from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.job import JobStatus


class JobCreate(BaseModel):
    payload: dict[str, Any] = Field(..., json_schema_extra={"example": {"task": "send_email", "to": "user@example.com"}})
    priority: int = Field(default=0, ge=0, le=10, description="Prioridade do job (0 = menor, 10 = maior)")


class JobUpdate(BaseModel):
    payload: dict[str, Any] = Field(..., json_schema_extra={"example": {"task": "send_email", "to": "user@example.com"}})
    priority: int = Field(ge=0, le=10)


class JobPatch(BaseModel):
    priority: int | None = Field(default=None, ge=0, le=10)
    requeue: bool | None = Field(default=None, description="Reenfileira o job se estiver como failed")


class JobResponse(BaseModel):
    id: UUID
    status: JobStatus
    payload: dict[str, Any]
    priority: int
    result: Any | None
    error: str | None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = {"from_attributes": True}


class JobCreatedResponse(BaseModel):
    job_id: UUID
    status: JobStatus
    message: str


class JobListResponse(BaseModel):
    total: int
    jobs: list[JobResponse]
