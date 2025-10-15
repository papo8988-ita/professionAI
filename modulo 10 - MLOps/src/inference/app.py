from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from src.model.hf_wrapper import HFLocalPredictor, log_prediction
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sentiment API")
predictor = HFLocalPredictor()

class InputText(BaseModel):
    text: str
    user_id: str = None
    metadata: dict = None

@app.post("/predict")
async def predict(payload: InputText, request: Request):
    res = predictor.predict(payload.text)
    # Log minimal: text (optionally hashed), model_version, metadata
    log_payload = {
        "text": payload.text,
        "user_id": payload.user_id,
        "metadata": payload.metadata,
        "prediction": res,
        "headers": dict(request.headers)
    }
    # fire-and-forget log
    try:
        log_prediction(log_payload)
    except Exception:
        pass
    return res

@app.get("/health")
def health():
    return {"status": "ok"}