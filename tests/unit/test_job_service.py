from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate
from app.services.job_service import JobService


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.save.side_effect = lambda job: job
    return repo


@pytest.fixture
def service(mock_repo):
    return JobService(mock_repo)


async def test_create_job(service, mock_repo):
    data = JobCreate(payload={"task": "test"}, priority=3)

    async def fake_save(job):
        job.status = JobStatus.PENDING
        return job

    mock_repo.save.side_effect = fake_save
    job = await service.create(data)

    assert job.status == JobStatus.PENDING
    assert job.payload == {"task": "test"}
    assert job.priority == 3
    mock_repo.save.assert_called_once()


async def test_get_by_id_not_found(service, mock_repo):
    mock_repo.find_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await service.get_by_id(uuid4())

    assert exc.value.status_code == 404


async def test_get_by_id_found(service, mock_repo):
    job = Job(id=str(uuid4()), payload={"task": "test"}, priority=0)
    mock_repo.find_by_id.return_value = job

    result = await service.get_by_id(job.id)
    assert result.id == job.id


async def test_list_all(service, mock_repo):
    jobs = [Job(id=str(uuid4()), payload={}, priority=0) for _ in range(3)]
    mock_repo.find_all.return_value = jobs

    total, result = await service.list_all()
    assert total == 3
    assert len(result) == 3


async def test_mark_processing(service, mock_repo):
    job = Job(id=str(uuid4()), payload={}, priority=0)
    mock_repo.find_by_id.return_value = job

    await service.mark_processing(job.id)
    assert job.status == JobStatus.PROCESSING
    assert job.started_at is not None


async def test_update_result(service, mock_repo):
    job = Job(id=str(uuid4()), payload={}, priority=0)
    mock_repo.find_by_id.return_value = job

    await service.update_result(job.id, {"processed": True})
    assert job.status == JobStatus.COMPLETED
    assert job.result == {"processed": True}


async def test_update_failure(service, mock_repo):
    job = Job(id=str(uuid4()), payload={}, priority=0)
    mock_repo.find_by_id.return_value = job

    await service.update_failure(job.id, "erro simulado")
    assert job.status == JobStatus.FAILED
    assert job.error == "erro simulado"
