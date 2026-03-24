<p align="center">
  <img src="FASTB.png" alt="realogom" width="610" />
</p>
<p align="center">
  <a href="https://github.com/cauaenzo/FAST-BACK/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0" /></a>
     <!-- Versão -->
  <img src="https://img.shields.io/badge/version-1.0.0-green" />

  <!-- Linguagem -->
  <img src="https://img.shields.io/badge/python-3.10-blue" />
</p>

Sistema de fila assíncrono construído com **FastAPI**, simulando o comportamento de ferramentas como RabbitMQ e Celery. Jobs são enfileirados, processados por workers assíncronos e têm seus status atualizados em tempo real.

---

## Arquitetura

```
app/
├── main.py              # Entry point FastAPI + lifespan
├── api/
│   ├── router.py        # Agregador de routers
│   └── v1/
│       └── jobs.py      # Endpoints de jobs
├── services/
│   └── job_service.py   # Regras de negócio
├── repositories/
│   └── job_repository.py # Persistência em memória
├── models/
│   └── job.py           # Modelo de domínio
├── schemas/
│   └── job.py           # Schemas Pydantic (request/response)
├── workers/
│   └── job_worker.py    # Worker assíncrono com asyncio.Queue
└── core/
    ├── config.py        # Configurações via .env
    └── logging.py       # Logger centralizado
```

---

## Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd Back-Fast

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
```

---

## Como rodar

```bash
python main.py
```

Ou diretamente com uvicorn:

```bash
uvicorn app.main:app --reload
```

Saída esperada no terminal:
```
API disponível em: http://127.0.0.1:8000
Swagger UI:        http://127.0.0.1:8000/docs
```

---

## Endpoints

| Método | Rota                  | Descrição              |
|--------|-----------------------|------------------------|
| POST   | `/api/v1/jobs`        | Cria e enfileira um job |
| GET    | `/api/v1/jobs`        | Lista todos os jobs    |
| GET    | `/api/v1/jobs/{id}`   | Consulta um job        |
| GET    | `/health`             | Health check           |

---

## Exemplos de uso

### Criar um job
```bash
curl -X POST http://127.0.0.1:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"payload": {"task": "send_email", "to": "user@example.com"}, "priority": 5}'
```

### Consultar status
```bash
curl http://127.0.0.1:8000/api/v1/jobs/{job_id}
```

### Listar todos
```bash
curl http://127.0.0.1:8000/api/v1/jobs
```

---

## Status dos jobs

| Status       | Descrição                        |
|--------------|----------------------------------|
| `pending`    | Aguardando na fila               |
| `processing` | Sendo processado pelo worker     |
| `completed`  | Processado com sucesso           |
| `failed`     | Falhou durante o processamento   |

---

## Configurações (.env)

| Variável              | Padrão | Descrição                          |
|-----------------------|--------|------------------------------------|
| `HOST`                | 127.0.0.1 | Host do servidor               |
| `PORT`                | 8000   | Porta do servidor                  |
| `WORKER_CONCURRENCY`  | 3      | Número de workers paralelos        |
| `JOB_PROCESSING_MIN`  | 1.0    | Tempo mínimo de processamento (s)  |
| `JOB_PROCESSING_MAX`  | 5.0    | Tempo máximo de processamento (s)  |
| `JOB_FAILURE_RATE`    | 0.1    | Taxa de falha simulada (0.0 - 1.0) |

---

## Documentação interativa

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
