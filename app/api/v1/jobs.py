from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobCreatedResponse, JobListResponse, JobResponse
from app.services.job_service import JobService
from app.workers.job_worker import enqueue

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_service(session: AsyncSession = Depends(get_session)) -> JobService:
    return JobService(JobRepository(session))


@router.post("", response_model=JobCreatedResponse, status_code=202)
async def create_job(data: JobCreate, service: JobService = Depends(get_service)):
    """Cria um novo job e o enfileira para processamento assíncrono."""
    job = await service.create(data)
    await enqueue(job.id)
    return JobCreatedResponse(job_id=job.id, status=job.status, message="Job enfileirado com sucesso")


@router.get("", response_model=JobListResponse)
async def list_jobs(service: JobService = Depends(get_service)):
    """Lista todos os jobs com seus status atuais."""
    total, jobs = await service.list_all()
    return JobListResponse(total=total, jobs=jobs)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: UUID, service: JobService = Depends(get_service)):
    """Consulta o status e resultado de um job específico."""
    return await service.get_by_id(job_id)
