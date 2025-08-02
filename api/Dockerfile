FROM python:3.12-slim

# RUN useradd -m safeuser -u 5000

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY api/app ./app

COPY uv.lock .
COPY pyproject.toml .

## RUN chown -R 5000:0 .
## USER safeuser

RUN uv sync --extra api

ENV PATH="/app/.venv/bin:$PATH"
CMD ["uv", "run", "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--reload", "--bind", "0.0.0.0:8000"]