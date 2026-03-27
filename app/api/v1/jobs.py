from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.core.database import get_session
from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobCreatedResponse, JobListResponse, JobResponse
from app.services.job_service import JobService
from app.workers.job_worker import enqueue

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_service(session: AsyncSession = Depends(get_session)) -> JobService:
    return JobService(JobRepository(session))


@router.post("", response_model=JobCreatedResponse, status_code=202)
async def create_job(
    data: JobCreate,
    service: JobService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """Cria um novo job e o enfileira para processamento assíncrono. Requer autenticação."""
    job = await service.create(data)
    await enqueue(job.id)
    return JobCreatedResponse(job_id=job.id, status=job.status, message="Job enfileirado com sucesso")


@router.get("", response_model=JobListResponse)
async def list_jobs(
    service: JobService = Depends(get_service),
    _: User = Depends(require_admin),
):
    """Lista todos os jobs. Requer role admin."""
    total, jobs = await service.list_all()
    return JobListResponse(total=total, jobs=jobs)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    service: JobService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """Consulta o status de um job. Requer autenticação."""
    return await service.get_by_id(job_id)
