import asyncio
import random
from uuid import UUID

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.logging import get_logger
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService

logger = get_logger(__name__)

_queue: asyncio.Queue[UUID] = asyncio.Queue()


async def enqueue(job_id: UUID) -> None:
    await _queue.put(job_id)
    logger.info(f"Job enfileirado | id={job_id} | queue_size={_queue.qsize()}")


async def _process(job_id: UUID) -> None:
    async with AsyncSessionLocal() as session:
        service = JobService(JobRepository(session))

        await service.mark_processing(job_id)
        logger.info(f"Processando job | id={job_id}")

        duration = random.uniform(settings.JOB_PROCESSING_MIN, settings.JOB_PROCESSING_MAX)
        await asyncio.sleep(duration)

        if random.random() < settings.JOB_FAILURE_RATE:
            await service.update_failure(job_id, "Falha simulada durante o processamento")
            logger.warning(f"Job falhou | id={job_id}")
        else:
            await service.update_result(job_id, {"processed": True, "duration_seconds": round(duration, 2)})
            logger.info(f"Job concluído | id={job_id} | duration={duration:.2f}s")


async def _worker(worker_id: int) -> None:
    logger.info(f"Worker {worker_id} iniciado")
    while True:
        job_id = await _queue.get()
        try:
            await _process(job_id)
        except Exception as exc:
            logger.error(f"Worker {worker_id} erro inesperado | id={job_id} | error={exc}")
        finally:
            _queue.task_done()


async def start_workers() -> None:
    for i in range(1, settings.WORKER_CONCURRENCY + 1):
        asyncio.create_task(_worker(i))
    logger.info(f"{settings.WORKER_CONCURRENCY} workers iniciados")
