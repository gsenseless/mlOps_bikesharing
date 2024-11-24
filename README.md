It is a model wrapped into the container, and orchestrated by Airflow, which predicts 'Rented Bike Count' based on bike sharing​ data. Data and MLflow artifacts are stored on AWS S3 (localstack actually).
To run it:
```
mkdir -p ./dags ./logs ./plugins ./config
```
set environmental variables with your AWS secrets:
```
export AWS_ACCESS_KEY_ID="your_access_key_id" AWS_SECRET_ACCESS_KEY="your_secret_access_key"
```
and with Airflow user ID:
```
export AIRFLOW_UI=$(id -u)
```

Prepare and start containers:
```
docker compose build
docker compose up airflow-init
docker compose up -d
```
Wait about a minute until all services will be up. Go to:
http://localhost:8080/ 
User and password are "airflow". Start DAG and view logs.
You can check MLflow as well: http://localhost:5000/

If you need to stop the containers:
```
docker compose down --volumes
```


[![tests](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml/badge.svg)](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml)
