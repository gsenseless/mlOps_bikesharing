FROM apache/airflow:3.0.3

#USER root

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

USER airflow

### temp workaround
# RUN python -m ensurepip --upgrade
# RUN python -m pip install --upgrade setuptools

WORKDIR /opt/airflow

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml ./
### uv sync doen't work with Airflow
#COPY uv.lock .

# Generate requirements.txt from pyproject.toml and install with system Python
RUN echo "apache-airflow==${AIRFLOW_VERSION}" > airflow-constraint.txt

RUN uv pip compile pyproject.toml --extra train --constraint airflow-constraint.txt --output-file requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt


