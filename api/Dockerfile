FROM python:3.10-slim

WORKDIR /app
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock for all dependencies
COPY Pipfile.lock .
COPY Pipfile .

# Install both shared and API-specific dependencies
RUN pipenv install --system --deploy --categories "packages api"

COPY api/app ./app

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--reload", "--bind", "0.0.0.0:8000"]