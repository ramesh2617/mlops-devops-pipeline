from fastapi import FastAPI
from app.schema import CustomerInput, PredictionResponse
from app.predict import ChurnPredictor

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0.0"
)

predictor = ChurnPredictor()


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(data: CustomerInput):
    return predictor.predict(data.dict())
