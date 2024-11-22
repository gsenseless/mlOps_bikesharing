FROM apache/airflow:2.9.3

#USER root

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

USER airflow
WORKDIR /opt/airflow

### temp workaround
RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade setuptools
RUN python -m pip install numpy==1.26.4

RUN pip install --no-cache-dir pipenv
COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
RUN pipenv install --deploy --system
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}"