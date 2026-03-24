from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Queue System API"
    APP_DESCRIPTION: str = "Sistema de fila assíncrono com processamento de jobs em background"
    APP_VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKER_CONCURRENCY: int = 3
    JOB_PROCESSING_MIN: float = 1.0
    JOB_PROCESSING_MAX: float = 5.0
    JOB_FAILURE_RATE: float = 0.1

    class Config:
        env_file = ".env"


settings = Settings()
