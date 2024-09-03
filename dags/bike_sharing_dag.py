import os
import pickle
from datetime import datetime
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from airflow.decorators import dag, task
from airflow.io.path import ObjectStoragePath


bucket_name = os.getenv("BUCKET_NAME")


@dag(
    schedule="@once",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    # wait_for_downstream=True,
    tags=["edu"],
)
def bikes_taskflow_api():
    @task
    def prepare_data() -> None:
        # fetch dataset
        from ucimlrepo import fetch_ucirepo

        data = fetch_ucirepo(id=560)
        data = data.data.features

        data = data.drop(columns=["Date"])
        data = data.select_dtypes(exclude=["object", "category"])

        # Define the feature set and target variable
        X = data.drop(columns=["Rented Bike Count"])  # Features
        y = data["Rented Bike Count"]  # Target variable

        data_split = train_test_split(X, y, test_size=0.2, random_state=52)

        logging.info(f"uploading data to s3 into {bucket_name} bucket")
        for name, data in zip(["train_x", "test_x", "train_y", "test_y"], data_split):
            data.to_csv(f"s3://{bucket_name}/{name}.csv")

        logging.info("data is saved to s3")
        return None

    @task
    def train_model() -> str:
        logging.info("loading data from s3")
        data = {}
        for name in ["train_x", "train_y"]:
            data[name] = pd.read_csv(f"s3://{bucket_name}/{name}.csv")

        logging.info("training the model")
        model = DecisionTreeRegressor()
        model.fit(data["train_x"], data["train_y"])

        logging.info("saving the model to s3")
        model_filename = "bike-sharing-model.pkl"
        base = ObjectStoragePath(f"s3://{bucket_name}", conn_id=None)
        path = base / model_filename
        with path.open("wb") as f:
            pickle.dump(model, f)

        return model_filename

    @task
    def evaluate_model(model_filename: str) -> None:
        logging.info("loading test data")
        data = {}
        for name in ["test_x", "test_y"]:
            data[name] = pd.read_csv(f"s3://{bucket_name}/{name}.csv")

        logging.info("loading the model")
        base = ObjectStoragePath(f"s3://{bucket_name}/")
        path = base / model_filename
        with path.open("rb") as f:
            model = pickle.load(f)

        predictions = model.predict(data["test_x"])
        mae = mean_absolute_error(data["test_y"], predictions)
        logging.info(f"Mean Absolute Error: {mae}")
        return None

    model_filename = train_model()
    evaluate_model(model_filename)
    prepare_data() >> model_filename


bikes_taskflow_api()
