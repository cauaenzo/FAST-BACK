<p align="center">
  <img src="FASTB.png" alt="realogom" width="610" />
</p>
<p align="center">
  <a href="https://github.com/cauaenzo/FAST-BACK/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/version-1.0.0-blueviolet?labelColor=blueviolet&style=flat" />
  <img src="https://img.shields.io/badge/python-3.12-green?labelColor=blue&style=flat" />
  <img src="https://img.shields.io/badge/docker-ready-2496ED?logo=docker&style=flat" />
  <img src="https://img.shields.io/badge/postgres-16-336791?logo=postgresql&style=flat" />
  <img src="https://img.shields.io/badge/performance-excellent-brightgreen?labelColor=brightgreen&style=flat" />
</p>

Sistema de fila assíncrono construído com **FastAPI** e **PostgreSQL**, containerizado com Docker. Jobs são enfileirados, processados por workers assíncronos e persistidos em banco de dados com status atualizado em tempo real.

---

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web assíncrono
- **[PostgreSQL 16](https://www.postgresql.org/)** — banco de dados relacional
- **[SQLAlchemy 2](https://docs.sqlalchemy.org/)** — ORM async
- **[Alembic](https://alembic.sqlalchemy.org/)** — migrations de banco
- **[pgAdmin 4](https://www.pgadmin.org/)** — interface visual do banco
- **[Docker](https://www.docker.com/)** — containerização completa
- **[Pydantic v2](https://docs.pydantic.dev/)** — validação de dados
- **[Uvicorn](https://www.uvicorn.org/)** — servidor ASGI

---

## Arquitetura

```
app/
├── main.py               # Entry point FastAPI + lifespan
├── api/
│   ├── router.py         # Agregador de routers
│   └── v1/
│       └── jobs.py       # Endpoints de jobs
├── services/
│   └── job_service.py    # Regras de negócio
├── repositories/
│   └── job_repository.py # Queries async com SQLAlchemy
├── models/
│   └── job.py            # Modelo ORM mapeado para o banco
├── schemas/
│   └── job.py            # Schemas Pydantic (request/response)
├── workers/
│   └── job_worker.py     # Worker assíncrono com asyncio.Queue
└── core/
    ├── config.py         # Configurações via .env
    ├── database.py       # Engine async e sessão do banco
    └── logging.py        # Logger centralizado
```

---

## Pré-requisitos

- [Docker](https://www.docker.com/) instalado
- [Docker Compose](https://docs.docker.com/compose/) instalado

---

## Instalação e execução

```bash
# Clone o repositório
git clone https://github.com/cauaenzo/FAST-BACK.git
cd Back-Fast

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# Suba todos os serviços
docker-compose up --build
```

Saída esperada no terminal:
```
API disponível em: http://0.0.0.0:8000
Swagger UI:        http://0.0.0.0:8000/docs
```

---

## Serviços

| Serviço   | URL                        | Descrição                  |
|-----------|----------------------------|----------------------------|
| API       | http://localhost:8000      | FastAPI                    |
| Swagger   | http://localhost:8000/docs | Documentação interativa    |
| ReDoc     | http://localhost:8000/redoc| Documentação alternativa   |
| pgAdmin   | http://localhost:5050      | Interface visual do banco  |

---

## Endpoints

### Auth

| Método | Rota                      | Descrição                        | Proteção |
|--------|---------------------------|----------------------------------|----------|
| POST   | `/api/v1/auth/register`   | Registra um novo usuário         | Pública  |
| POST   | `/api/v1/auth/login`      | Autentica e retorna token JWT    | Pública  |

### Jobs

| Método | Rota                  | Descrição               | Proteção        |
|--------|-----------------------|-------------------------|-----------------|
| POST   | `/api/v1/jobs`        | Cria e enfileira um job | Autenticado     |
| GET    | `/api/v1/jobs`        | Lista todos os jobs     | Admin           |
| GET    | `/api/v1/jobs/{id}`   | Consulta um job         | Autenticado     |
| GET    | `/health`             | Health check            | Pública         |

---

## Exemplos de uso

### Registrar usuário
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha123"}'
```

### Login e obter token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha123"}'
```

### Criar um job
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"payload": {"task": "send_email", "to": "user@example.com"}, "priority": 5}'
```

### Consultar status
```bash
curl http://localhost:8000/api/v1/jobs/{job_id} \
  -H "Authorization: Bearer SEU_TOKEN"
```

### Listar todos (admin)
```bash
curl http://localhost:8000/api/v1/jobs \
  -H "Authorization: Bearer SEU_TOKEN_ADMIN"
```

---

## Status dos jobs

| Status       | Descrição                      |
|--------------|--------------------------------|
| `pending`    | Aguardando na fila             |
| `processing` | Sendo processado pelo worker   |
| `completed`  | Processado com sucesso         |
| `failed`     | Falhou durante o processamento |

---

## Configurações (.env)

| Variável             | Descrição                                        |
|----------------------|--------------------------------------------------|
| `HOST`               | Host do servidor                                 |
| `PORT`               | Porta do servidor                                |
| `WORKER_CONCURRENCY` | Número de workers paralelos                      |
| `JOB_PROCESSING_MIN` | Tempo mínimo de processamento (s)                |
| `JOB_PROCESSING_MAX` | Tempo máximo de processamento (s)                |
| `JOB_FAILURE_RATE`   | Taxa de falha simulada (0.0 - 1.0)               |
| `POSTGRES_USER`      | Usuário do banco                                 |
| `POSTGRES_PASSWORD`  | Senha do banco                                   |
| `POSTGRES_DB`        | Nome do banco                                    |
| `POSTGRES_HOST`      | Host do banco (padrão: postgres)                 |
| `POSTGRES_PORT`      | Porta do banco (padrão: 5432)                    |
| `PGADMIN_EMAIL`      | Email de acesso ao pgAdmin                       |
| `PGADMIN_PASSWORD`   | Senha de acesso ao pgAdmin                       |
| `JWT_SECRET_KEY`     | Chave secreta para assinar tokens JWT            |
| `JWT_ALGORITHM`      | Algoritmo JWT (padrão: HS256)                    |
| `JWT_EXPIRE_MINUTES` | Tempo de expiração do token em minutos           |
| `ADMIN_USERNAME`     | Usuário admin criado no primeiro startup         |
| `ADMIN_PASSWORD`     | Senha admin criada no primeiro startup           |

---

## Testes

O projeto conta com dois tipos de testes:

- **Unitários** — testam o `JobService` isolado com repositório mockado, validando as regras de negócio
- **Integração** — testam os endpoints HTTP completos com banco SQLite em memória

```
tests/
├── conftest.py              # fixtures compartilhadas
├── unit/
│   └── test_job_service.py  # testes do service
└── integration/
    └── test_jobs_api.py     # testes dos endpoints
```

### Rodar localmente

```bash
venv\Scripts\python.exe -m pytest tests/ -v
```

### Rodar via Docker

```bash
docker-compose --profile test run --rm test
```

---

## pgAdmin

Acesse `http://localhost:5050` e conecte ao servidor com:

- **Host:** `postgres`
- **Port:** `5432`
- **Database:** valor de `POSTGRES_DB`
- **Username:** valor de `POSTGRES_USER`
- **Password:** valor de `POSTGRES_PASSWORD`

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais informações.
