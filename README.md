It is a model wrapped into the container, and orchestrated by Airflow, which predicts 'Rented Bike Count' based on bike sharing​ data. Data and MLflow artifacts are stored on S3 (localstack).

## Setup

### Prerequisites
```
mkdir -p ./dags ./logs ./plugins ./config
```
Set environmental variables with your AWS secrets:
```
export AWS_ACCESS_KEY_ID="your_access_key_id" AWS_SECRET_ACCESS_KEY="your_secret_access_key"
```
and with Airflow user ID:
```
export AIRFLOW_UID=$(id -u)
```

### Starting the Services
Prepare and start containers:
```
docker compose build
docker compose up airflow-init
docker compose up -d
```
Wait about a minute until all services will be up.

### Accessing Services
- **Airflow**: http://localhost:8080/ (user/password: "airflow")
- **MLflow**: http://localhost:5000/
- **Prediction API**: http://localhost:8000/

### Using the Prediction API
The prediction service provides the following endpoints:
- `GET /health`: Check service health
- `POST /predict`: Make predictions using the following JSON format:

Feature descriptions:
- `hour`: Hour of the day (0-23)
- `temperature`: Temperature in Celsius
- `humidity`: Humidity percentage (0-100)
- `wind_speed`: Wind speed in m/s
- `visibility`: Visibility in km
- `dew_point_temperature`: Dew point temperature in Celsius
- `solar_radiation`: Solar radiation in MJ/m2
- `rainfall`: Rainfall in mm
- `snowfall`: Snowfall in cm

Example curl request:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "hour": 12,
           "temperature": 20.5,
           "humidity": 65,
           "wind_speed": 2.5,
           "visibility": 2000,
           "dew_point_temperature": 15.5,
           "solar_radiation": 1.2,
           "rainfall": 0,
           "snowfall": 0
         }'
```

### Stopping Services
To stop all containers:
```
docker compose down --volumes
```

[![tests](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml/badge.svg)](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml)
