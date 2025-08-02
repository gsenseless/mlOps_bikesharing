import os

# import pickle
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
import mlflow
import mlflow.sklearn
from ucimlrepo import fetch_ucirepo


BUCKET_NAME = os.getenv("BUCKET_NAME")
EXPERIMENT_NAME = "bike_sharing_experiment"
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))


def prepare_data(data_bucket_name: str = BUCKET_NAME) -> None:
    """Prepare and split the bike sharing dataset for training and testing.
    
    This function fetches the bike sharing dataset from UCI repository, preprocesses
    the data by removing non-numeric columns and the Date column, splits the data
    into training and testing sets, and uploads the split datasets to S3.
    
    Args:
        data_bucket_name (str): The name of the S3 bucket where the data will be stored.
                               Defaults to the BUCKET_NAME environment variable.
    
    Returns:
        None: This function doesn't return any value but uploads data to S3.
    
    Note:
        The function creates four CSV files in S3:
        - train_x.csv: Training features
        - test_x.csv: Testing features  
        - train_y.csv: Training target variable
        - test_y.csv: Testing target variable
    """
    # fetch dataset

    data = fetch_ucirepo(id=560)
    data = data.data.features

    data = data.drop(columns=["Date"])
    data = data.select_dtypes(exclude=["object", "category"])

    # Define the feature set and target variable
    X = data.drop(columns=["Rented Bike Count"])  # Features
    y = data["Rented Bike Count"]  # Target variable

    data_split = train_test_split(X, y, test_size=0.2, random_state=52)

    logging.info(f"uploading data to s3 into {data_bucket_name} bucket")
    for name, data in zip(["train_x", "test_x", "train_y", "test_y"], data_split):
        data.to_csv(f"s3://{data_bucket_name}/{name}.csv", index=False)

    logging.info("data is saved to s3")

    return None


def train_model(data_bucket_name: str = BUCKET_NAME) -> str:
    """Train a Decision Tree model for bike sharing prediction.
    
    This function loads the training data from S3, trains a Decision Tree Regressor
    model with MLflow tracking, logs the model artifacts, and registers the model
    in MLflow Model Registry.
    
    Args:
        data_bucket_name (str): The name of the S3 bucket containing the training data.
                               Defaults to the BUCKET_NAME environment variable.
    
    Returns:
        str: The name of the registered model in MLflow Model Registry.
    """
    MODEL_NAME = os.getenv("MODEL_NAME")

    logging.info("loading data from s3")
    data = {}
    for name in ["train_x", "train_y"]:
        data[name] = pd.read_csv(f"s3://{data_bucket_name}/{name}.csv")

    logging.info(f"mlflow tracking URI: {mlflow.get_tracking_uri()}")
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.autolog()
    with mlflow.start_run() as run:
        logging.info("training the model")
        model = DecisionTreeRegressor(max_depth=3)
        model.fit(data["train_x"], data["train_y"])

        mlflow.sklearn.log_model(model, artifact_path="bike-sharing")
        mlflow.register_model(f"runs:/{run.info.run_id}/bike-sharing", MODEL_NAME)
        logging.info("Model logged and registered successfully")

    # logging.info("saving the model to s3")
    # model_filename = "bike-sharing-model.pkl"
    # base = ObjectStoragePath(f"s3://{data_bucket_name}", conn_id=None)
    # path = base / model_filename
    # with path.open("wb") as f:
    #     pickle.dump(model, f)

    return MODEL_NAME


def evaluate_model(model_name: str, data_bucket_name: str = BUCKET_NAME) -> None:
    """Evaluate the trained bike sharing model on test data.
    
    This function loads the test data from S3, loads the latest version of the
    trained model from MLflow Model Registry, makes predictions on the test set,
    and calculates the Mean Absolute Error (MAE) to assess model performance.
    
    Args:
        model_name (str): The name of the model in MLflow Model Registry to evaluate.
        data_bucket_name (str): The name of the S3 bucket containing the test data.
                               Defaults to the BUCKET_NAME environment variable.
    
    Returns:
        None: This function doesn't return any value but logs the evaluation metrics.
    """
    logging.info("loading test data")
    data = {}
    for name in ["test_x", "test_y"]:
        data[name] = pd.read_csv(f"s3://{data_bucket_name}/{name}.csv")

    logging.info("loading the modelfrom MLflow")
    model_uri = f"models:/{model_name}/latest"
    model = mlflow.sklearn.load_model(model_uri)
    logging.info("Latest model loaded successfully")

    # base = ObjectStoragePath(f"s3://{data_bucket_name}/")
    # path = base / model_filename
    # with path.open("rb") as f:
    #     model = pickle.load(f)

    predictions = model.predict(data["test_x"])
    mae = mean_absolute_error(data["test_y"], predictions)
    logging.info(f"Mean Absolute Error: {mae}")

    return None
