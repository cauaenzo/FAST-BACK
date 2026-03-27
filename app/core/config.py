from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Queue System API"
    APP_DESCRIPTION: str = "Sistema de fila assíncrono com processamento de jobs em background"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKER_CONCURRENCY: int = 3
    JOB_PROCESSING_MIN: float = 1.0
    JOB_PROCESSING_MAX: float = 5.0
    JOB_FAILURE_RATE: float = 0.1

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    PGADMIN_EMAIL: str = "admin@admin.com"
    PGADMIN_PASSWORD: str = "admin123"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
