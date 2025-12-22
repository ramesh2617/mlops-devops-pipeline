import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Create model directory if not exists
os.makedirs("models", exist_ok=True)

# Set MLflow experiment
mlflow.set_experiment("iris-mlops")

# Load data
X, y = load_iris(return_X_y=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

with mlflow.start_run():
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    mlflow.log_metric("accuracy", accuracy)

    # Save model locally
    joblib.dump(model, "models/model.pkl")

    # Log model to MLflow
    mlflow.sklearn.log_model(model, artifact_path="model")

    print(f"Model trained with accuracy: {accuracy}")
