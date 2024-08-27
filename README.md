It is a model wrapped into the container, and orchestrated by Airflow, which predicts 'Rented Bike Count' based on bike sharing​ data. Data is stored on AWS S3 (localstack actually).
To run it:
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
fill in .env file with AWS credentials like so:
```
AWS_ACCESS_KEY_ID='xxxxxxxxxxx'
AWS_SECRET_ACCESS_KEY='xxxxxxxxxxx'
AWS_ENDPOINT_URL='http://localstack:4566/'
AWS_DEFAULT_REGION='us-east-1'
BUCKET_NAME='bike-sharing-model'
```
you can do it using this command
```
echo -e "\nAWS_ACCESS_KEY_ID='xxxxxxxxxxx'\nAWS_SECRET_ACCESS_KEY='xxxxxxxxxxx'\nAWS_ENDPOINT_URL='http://localstack:4566/'\nAWS_DEFAULT_REGION='us-east-1'\nBUCKET_NAME='bike-sharing-model'" >> .env
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
