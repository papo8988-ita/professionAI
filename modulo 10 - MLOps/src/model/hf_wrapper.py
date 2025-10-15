from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time
import os
import numpy as np
import json
import pandas as pd
import requests

# === CONFIG ===
# Carica prima il percorso del modello salvato (se presente), altrimenti il nome base
MODEL_PATH = os.getenv("MODEL_PATH", "outputs/model_pretrained")
MODEL_NAME = os.getenv("MODEL_NAME", "cardiffnlp/twitter-roberta-base-sentiment-latest")
LOG_COLLECTOR = os.getenv("LOG_COLLECTOR", None)
LOCAL_LOG_PATH = os.getenv("LOCAL_LOG_PATH", "logs/inference_logs.parquet")


class HFLocalPredictor:
    def __init__(self, model_name_or_path=None, device=None):
        # Se il percorso salvato esiste, usalo. Altrimenti, fallback al modello online.
        model_source = model_name_or_path or (
            MODEL_PATH if os.path.exists(MODEL_PATH) else MODEL_NAME
        )

        print(f"Caricamento modello da: {model_source}")

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_source)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_source)
        self.model.to(self.device)
        self.model.eval()

        # mapping di labels secondo model card: 0 negative, 1 neutral, 2 positive
        self.id2label = {0: "negative", 1: "neutral", 2: "positive"}

    def predict(self, text: str):
        """Esegue una predizione di sentiment su una stringa di testo."""
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()[0].tolist()
            label_idx = int(logits.argmax(-1).cpu().item())

        return {
            "label": self.id2label[label_idx],
            "label_idx": label_idx,
            "probs": probs,
            "timestamp": time.time()
        }


def sanitize_payload(payload: dict):
    """Converte tutti i tipi non serializzabili in stringhe."""
    clean = {}
    for k, v in payload.items():
        try:
            if isinstance(v, (dict, list)):
                clean[k] = json.dumps(v)
            elif isinstance(v, (int, float, str)) or v is None:
                clean[k] = v
            else:
                clean[k] = str(v)
        except Exception:
            clean[k] = str(v)
    return clean


def log_prediction_local(payload: dict):
    try:
        clean_payload = sanitize_payload(payload)
        df = pd.DataFrame([clean_payload])

        os.makedirs(os.path.dirname(LOCAL_LOG_PATH), exist_ok=True)

        # Scrivi o append
        if not os.path.exists(LOCAL_LOG_PATH):
            df.to_parquet(LOCAL_LOG_PATH, index=False)
        else:
            existing = pd.read_parquet(LOCAL_LOG_PATH)
            df_all = pd.concat([existing, df], ignore_index=True)
            df_all.to_parquet(LOCAL_LOG_PATH, index=False)

        print(f"Log salvato in {LOCAL_LOG_PATH}")
    except Exception as e:
        print(f"Errore nel salvataggio del log: {e}")

def log_prediction(payload: dict):
    """
    Proxy per inviare al collector remoto e salvare localmente.
    """
    # salva localmente (sempre)
    log_prediction_local(payload)

    # se definito il collector remoto, invia
    if LOG_COLLECTOR:
        try:
            requests.post(LOG_COLLECTOR, json=payload, timeout=2)
        except Exception:
            pass