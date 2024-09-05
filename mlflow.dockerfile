FROM python:3.10-slim

WORKDIR /mlflow

RUN pip install mlflow

EXPOSE 5000

CMD [ \
    "mlflow", "server", \ 
    "--backend-store-uri", "sqlite:///mlflow.db", \
    #--backend-store-uri postgresql://<<MLFLOW_USER>>:<<PASSWORD>>!@<<IP_ADDRESS>>:5432/<<MLFLOW_DB>>
    "--default-artifact-root", "s3://mlflow-bucket", \
    "--host", "0.0.0.0", \
    "--port", "5000" \
]
