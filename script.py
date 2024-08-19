from ucimlrepo import fetch_ucirepo
import pandas as pd
from sklearn.model_selection import train_test_split

# from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error


def prepare_data() -> tuple:
    # fetch dataset
    seoul_bike_sharing_demand = fetch_ucirepo(id=560)
    data = seoul_bike_sharing_demand.data.features
    data = data.drop(columns=["Date"])
    data = data.select_dtypes(exclude=["object", "category"])

    # Define the feature set and target variable
    X = data.drop(columns=["Rented Bike Count"])  # Features
    y = data["Rented Bike Count"]  # Target variable

    train_x, test_x, train_y, test_y = train_test_split(
        X, y, test_size=0.2, random_state=52
    )
    return train_x, test_x, train_y, test_y


def train_model(train_x: pd.DataFrame, train_y: pd.Series) -> DecisionTreeRegressor:
    model = DecisionTreeRegressor()
    model.fit(train_x, train_y)
    return model


def evaluate_model(
    model: DecisionTreeRegressor, test_x: pd.DataFrame, test_y: pd.Series
) -> None:
    predictions = model.predict(test_x)
    mae = mean_absolute_error(test_y, predictions)
    print(f"Mean Absolute Error: {mae}")


def main():
    train_x, test_x, train_y, test_y = prepare_data()
    model = train_model(train_x, train_y)
    evaluate_model(model, test_x, test_y)


if __name__ == "__main__":
    main()
