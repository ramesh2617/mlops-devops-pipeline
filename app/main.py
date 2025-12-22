from fastapi import FastAPI
import joblib
import os
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="MLOps Model API")

# Load model
MODEL_PATH = "models/model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found. Train the model first.")

model = joblib.load(MODEL_PATH)

# Input schema
class IrisInput(BaseModel):
    features: list[float]

@app.get("/")
def health_check():
    return {"status": "Model API is running"}

@app.post("/predict")
def predict(data: IrisInput):
    prediction = model.predict([data.features])
    return {"prediction": int(prediction[0])}
