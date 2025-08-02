FROM python:3.10-slim

WORKDIR /mlflow

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

### TODO: add as optinal dependency to pyproject
RUN uv pip install --system --no-cache-dir mlflow

EXPOSE 5000

CMD [ \
    "uv", "run", "mlflow", "server", \ 
    "--backend-store-uri", "sqlite:///mlflow.db", \
    #--backend-store-uri postgresql://<<MLFLOW_USER>>:<<PASSWORD>>!@<<IP_ADDRESS>>:5432/<<MLFLOW_DB>>
    "--default-artifact-root", "s3://mlflow-bucket", \
    "--host", "0.0.0.0", \
    "--port", "5000" \
]
