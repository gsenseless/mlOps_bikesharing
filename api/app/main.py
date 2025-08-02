import logging
import os

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="Bike Sharing Prediction API",
    description="API for predicting bike sharing demand using MLflow model",
    version="1.0.0",
)


# Define input schema
class PredictionInput(BaseModel):
    hour: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity in percentage")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    visibility: float = Field(..., ge=0, description="Visibility in 10m")
    dew_point_temperature: float = Field(
        ..., description="Dew point temperature in Celsius"
    )
    solar_radiation: float = Field(..., ge=0, description="Solar radiation in MJ/m2")
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")
    snowfall: float = Field(..., ge=0, description="Snowfall in cm")

    class Config:
        schema_extra = {
            "example": {
                "hour": 12,
                "temperature": 20.5,
                "humidity": 65,
                "wind_speed": 2.5,
                "visibility": 2000,
                "dew_point_temperature": 15.5,
                "solar_radiation": 1.2,
                "rainfall": 0,
                "snowfall": 0,
            }
        }


def load_model():
    """Load the MLflow model."""
    try:
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
        model_uri = f"models:/{os.environ['MODEL_NAME']}/latest"
        logger.info("Loading model from %s", model_uri)
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        logger.error("Error loading model: %s", str(e))
        return None


@app.get("/")
async def root():
    return {
        "message": "Welcome to Bike Sharing Prediction API."
        "Use curl request described in README.md."
        "Or check localhost:8000/health"
    }


@app.get("/health")
async def health_check():
    model = load_model()
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model exists in MLflow by:\n"
            "1. Open Airflow UI at http://localhost:8080 \n "
            "2. Login with airflow/airflow \n "
            "3. Find and trigger the bike_sharing_dag to train and register the model",
        )
    return {
        "status": "healthy",
        "model_loaded": True,
        "mlflow_tracking_uri": os.environ["MLFLOW_TRACKING_URI"],
    }


@app.post("/predict")
async def predict(input_data: PredictionInput):
    model = load_model()
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model exists in MLflow by:\n"
            "1. Open Airflow UI at http://localhost:8080\n"
            "2. Login with airflow/airflow\n"
            "3. Find and trigger the bike_sharing_dag to train and register the model",
        )

    try:
        # Convert input to DataFrame with proper feature order
        features = pd.DataFrame(
            [
                {
                    "Hour": input_data.hour,
                    "Temperature": input_data.temperature,
                    "Humidity": input_data.humidity,
                    "Wind speed": input_data.wind_speed,
                    "Visibility": input_data.visibility,
                    "Dew point temperature": input_data.dew_point_temperature,
                    "Solar Radiation": input_data.solar_radiation,
                    "Rainfall": input_data.rainfall,
                    "Snowfall": input_data.snowfall,
                }
            ]
        )

        prediction = model.predict(features)

        return {"prediction": float(prediction[0]), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
