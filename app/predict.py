import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("models/model.pkl")


class ChurnPredictor:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError("Model file not found. Train the model first.")
        self.model = joblib.load(MODEL_PATH)

    def predict(self, data: dict):
        df = pd.DataFrame([data])

        # Predict probability
        prob = self.model.predict_proba(df)[0][1]
        pred = int(prob >= 0.5)

        return {
            "churn_probability": round(prob, 4),
            "churn_prediction": pred
        }
