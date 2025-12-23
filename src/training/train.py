import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

import mlflow
import mlflow.sklearn


# Paths
PROCESSED_DATA_PATH = Path("data/processed.csv")
MODEL_OUTPUT_PATH = Path("models/model.pkl")

# MLflow setup
mlflow.set_experiment("customer-churn-prediction")


def load_processed_data():
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError("Processed data not found. Run preprocessing first.")
    return pd.read_csv(PROCESSED_DATA_PATH)


def train_model():
    # Load data
    df = load_processed_data()

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model
    model = LogisticRegression(max_iter=1000)

    # Start MLflow run
    with mlflow.start_run():
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("roc_auc", roc_auc)

        # Log model
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Save model locally
        MODEL_OUTPUT_PATH.parent.mkdir(exist_ok=True)
        joblib.dump(model, MODEL_OUTPUT_PATH)

        print("Model training completed")
        print(f"Accuracy: {accuracy}")
        print(f"ROC AUC: {roc_auc}")
        print(f"Model saved to: {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    train_model()
