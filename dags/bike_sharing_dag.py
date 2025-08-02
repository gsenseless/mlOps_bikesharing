from datetime import datetime
from airflow.decorators import dag, task
from airflow.io.path import ObjectStoragePath


@dag(
    schedule="@once",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["edu"],
)
def bikes_taskflow_api():
    @task
    def prepare_data() -> None:
        from source.bike_sharing import prepare_data

        prepare_data()
        return None

    @task
    def train_model() -> str:
        from source.bike_sharing import train_model

        model_name = train_model()
        return model_name

    @task
    def evaluate_model(model_name: str) -> None:
        from source.bike_sharing import evaluate_model

        evaluate_model(model_name)
        return None

    model_name = train_model()
    evaluate_model(model_name)
    prepare_data() >> model_name


bikes_taskflow_api()
