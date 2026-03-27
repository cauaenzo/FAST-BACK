import pytest


async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_create_job(client):
    response = await client.post(
        "/api/v1/jobs",
        json={"payload": {"task": "send_email"}, "priority": 2},
    )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"
    assert "job_id" in data


async def test_create_job_invalid_priority(client):
    response = await client.post(
        "/api/v1/jobs",
        json={"payload": {"task": "test"}, "priority": 99},
    )
    assert response.status_code == 422


async def test_list_jobs_empty(client):
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "jobs" in data


async def test_list_jobs_after_create(client):
    await client.post("/api/v1/jobs", json={"payload": {"task": "test"}, "priority": 0})
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


async def test_get_job_by_id(client):
    create = await client.post("/api/v1/jobs", json={"payload": {"task": "test"}, "priority": 1})
    job_id = create.json()["job_id"]

    response = await client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] == job_id


async def test_get_job_not_found(client):
    response = await client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
