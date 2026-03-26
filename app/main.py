from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.banner import print_banner
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import get_logger
from app.workers.job_worker import start_workers

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print_banner()
    logger.info("Iniciando aplicação...")
    await start_workers()
    logger.info(f"API disponível em: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"Swagger UI:        http://{settings.HOST}:{settings.PORT}/docs")
    yield
    await engine.dispose()
    logger.info("Encerrando aplicação...")


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
