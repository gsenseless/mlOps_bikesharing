It is a model that predicts 'Rented Bike Count' based on bike sharing data.

## Setup

### Prerequisites
```
mkdir -p ./logs ./plugins ./config
```
Set environment variables with your AWS secrets:
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
Wait about two minutes until all services are up.

### Accessing Services
- **Airflow**: http://localhost:8080/ (user/password: "airflow")
- **MLflow**: http://localhost:5000/
- **Prediction API**: http://localhost:8000/


Go to the Airflow UI and trigger or turn on the "bikes_taskflow_api" DAG. Go to the DAG tasks log. After jobs are complete, you can check the model metric (Mean Absolute Error):
<img width="1170" height="551" alt="image" src="https://github.com/user-attachments/assets/f6105c19-63dc-4ebc-bad8-7eca55ce9986" />

After that you should see a model registered in the MLflow models section.

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
docker compose down --volumes --remove-orphans
```

## Code Quality
To set up pre-commit hooks:
```bash
chmod +x scripts/setup-precommit.sh
./scripts/setup-precommit.sh
```
### Pre-commit Hooks
The project uses pre-commit hooks with:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting and style checking
```

Notes:
- Workflow is orchestrated by Apache Airflow.
- LocalStack (a cloud emulator) for S3 storage is used.
- The model deployment is containerized and could be deployed to the cloud.
- Model is registered in the MLflow Model Registry.
- Unit tests are present in dags/tests/
- GitHub Actions CI/CD pipeline is used.



[![tests](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml/badge.svg)](https://github.com/gsenseless/mlOps_bikesharing/actions/workflows/CI.yml)
