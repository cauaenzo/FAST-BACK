from uuid import UUID

from fastapi import APIRouter

from app.repositories.job_repository import job_repository
from app.schemas.job import JobCreate, JobCreatedResponse, JobListResponse, JobResponse
from app.services.job_service import JobService
from app.workers.job_worker import enqueue

router = APIRouter(prefix="/jobs", tags=["Jobs"])
_service = JobService(job_repository)


@router.post("", response_model=JobCreatedResponse, status_code=202)
async def create_job(data: JobCreate):
    """Cria um novo job e o enfileira para processamento assíncrono."""
    job = _service.create(data)
    await enqueue(job.id)
    return JobCreatedResponse(
        job_id=job.id,
        status=job.status,
        message="Job enfileirado com sucesso",
    )


@router.get("", response_model=JobListResponse)
def list_jobs():
    """Lista todos os jobs com seus status atuais."""
    total, jobs = _service.list_all()
    return JobListResponse(total=total, jobs=jobs)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: UUID):
    """Consulta o status e resultado de um job específico."""
    return _service.get_by_id(job_id)
