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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" pandas
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" "scikit-learn"
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" mlflow
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" "numpy==1.26.4"
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" "s3fs==2024.6.1"
RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" boto3

RUN uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" ucimlrepo


#ENV UV_PROJECT_ENVIRONMENT="~/.local"

#COPY uv.lock .
#COPY pyproject.toml .

# RUN /home/airflow/.local/bin/python3 -m uv sync --extra train
# RUN /home/airflow/.local/bin/python3 -m uv pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}"

#RUN uv pip install --system --no-deps --require-hashes --extra train ./uv.lock
