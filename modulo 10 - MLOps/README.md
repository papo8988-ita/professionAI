# Sentiment Analysis Pipeline con Hugging Face, MLflow e FastAPI

Questo progetto implementa una pipeline completa di analisi del sentiment su testi provenienti dai social media, basata su un modello RoBERTa fornito da Hugging Face.  
Include funzionalità di addestramento, inferenza, monitoraggio delle performance e deploy automatico come API e modello pubblicato su Hugging Face Hub.

---

## Descrizione generale

L’obiettivo del progetto è fornire un sistema di Machine Learning MLOps-ready per l’analisi del sentiment (positivo, neutro, negativo), che consenta:

- l’addestramento o il riutilizzo di un modello pre-addestrato;  
- il tracciamento esperimenti tramite MLflow;  
- la fornitura di un endpoint REST per inferenza via FastAPI;  
- il monitoraggio delle performance tramite Evidently;  
- l’automazione del deploy su Hugging Face Hub con GitHub Actions.

---

## Funzionalità principali

### 1. Addestramento o utilizzo modello pre-addestrato

Lo script `src/train.py` permette di scegliere tra due modalità operative:

- **fine_tune**: esegue il fine-tuning del modello base `cardiffnlp/twitter-roberta-base-sentiment-latest` sul dataset `tweet_eval/sentiment`, registrando automaticamente metriche e parametri su MLflow.  
- **pretrained**: utilizza direttamente il modello pre-addestrato senza training aggiuntivo, utile per test rapidi o deploy immediato.

La modalità si definisce nel file `.env` impostando una delle seguenti variabili:

TRAIN_MODE=fine_tune  
oppure  
TRAIN_MODE=pretrained

---

### 2. Logging e tracciamento con MLflow

Durante l’addestramento, il sistema registra:
- parametri di training;  
- metriche di accuratezza e F1-score;  
- artefatti del modello salvati con mlflow.pytorch.log_model.

Configurazione nel file `.env`:

MLFLOW_TRACKING_URI=mlruns  
MLFLOW_EXPERIMENT=sentiment-pipeline

---

### 3. API di inferenza con FastAPI

Il file `src/inference/app.py` espone un endpoint per le predizioni.

**Endpoint:** POST /predict

Esempio di richiesta JSON:

{
  "text": "Oggi è una giornata fantastica!",
  "user_id": "utente123",
  "metadata": {"source": "twitter"}
}

Esempio di risposta JSON:

{
  "label": "positive",
  "label_idx": 2,
  "probs": [0.01, 0.10, 0.89],
  "timestamp": 1698765432.12
}

Per avviare il servizio FastAPI eseguire:

uvicorn src.inference.app:app --host 0.0.0.0 --port 8000

Le predizioni vengono salvate come file `.parquet` nella cartella `logs/`, utili per il monitoraggio.

---

### 4. Monitoraggio con Evidently

Lo script `monitor_evidently.py` genera un report di data drift confrontando:
- il dataset di riferimento (`tweet_eval/validation`);  
- i log di inferenza più recenti.

Esecuzione:

python monitor_evidently.py

Il report viene salvato in:

monitor_reports/evidently_report.html

---

### 5. Deploy su Hugging Face Hub

Lo script `deploy_to_hub.py` automatizza la pubblicazione del modello e dei file associati su Hugging Face Hub.

Configurare il file `.env` con le credenziali personali:

HF_TOKEN=your_huggingface_token  
HF_USERNAME=your_username  
HF_MODEL_REPO=your_username/sentiment-model

Eseguire il comando:

python deploy_to_hub.py

Lo script esegue:
1. Login a Hugging Face CLI.  
2. Creazione o aggiornamento del repository del modello.  
3. Upload dei file (`config.json`, `model.safetensors`, `tokenizer`, `README.md`).

---

### 6. Pipeline CI/CD con GitHub Actions

Il file `.github/workflows/deploy.yml` definisce una pipeline CI/CD che:
1. Installa le dipendenze del progetto.  
2. Esegue test di integrazione.  
3. Effettua automaticamente il deploy del modello su Hugging Face Hub quando viene effettuato un push sul branch `main`.

---

## Configurazione del file `.env`

Un file `.env` deve contenere le variabili seguenti:

MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest  
OUTPUT_DIR=outputs  
MLFLOW_TRACKING_URI=mlruns  
MLFLOW_EXPERIMENT=sentiment-pipeline  
TRAIN_MODE=pretrained  
HF_TOKEN=your_huggingface_token  
HF_USERNAME=your_username  
HF_MODEL_REPO=your_username/sentiment-model  
INFERENCE_LOGS_PATH=logs/inference.parquet  
MONITOR_OUTPUT_DIR=monitor_reports  

---

## Requisiti principali

- Python >= 3.9  
- torch  
- transformers  
- datasets  
- mlflow  
- fastapi  
- uvicorn  
- evidently  
- huggingface_hub  
- python-dotenv  
- pandas, numpy  

Per installare tutte le dipendenze:

pip install -r requirements.txt

---

## Flusso operativo completo

1. **Configurazione del progetto**  
   Impostare le variabili nel file `.env` e verificare l’esistenza delle cartelle `outputs/` e `logs/`.

2. **Esecuzione del training o caricamento modello**  
   python src/train.py

3. **Avvio API di inferenza**  
   uvicorn src.inference.app:app --host 0.0.0.0 --port 8000

4. **Predizioni via API**  
   Inviare richieste POST a `/predict` con testo e metadati in input.

5. **Monitoraggio**  
   python monitor_evidently.py

6. **Deploy su Hugging Face**  
   python deploy_to_hub.py

---

## Architettura del sistema

               +----------------------+
               |     Dataset (HF)     |
               +----------+-----------+
                          |
                          v
               +----------------------+
               |     Training (MLflow)|
               +----------+-----------+
                          |
                          v
               +----------------------+
               |    Modello salvato   |
               |     outputs/         |
               +----------+-----------+
                          |
          +---------------+------------------+
          |                                  |
          v                                  v
    +-----------------------+        +----------------------+
    |  FastAPI Inference API|        | Monitor Evidently    |
    |  /predict endpoint    |        | Report drift         |
    +-----------+-----------+        +----------+-----------+
                |                                 |
       +----------------+             +----------------------+
       |  Logs (Parquet)|             | Report HTML          |
       +----------------+             +----------------------+
                              |
                              v
                   +----------------------+
                   | Deploy su HuggingFace|
                   +----------------------+

---

## Licenza

Questo progetto è distribuito sotto licenza **Apache 2.0**.  
È consentito il riutilizzo e la modifica a fini accademici e di ricerca.

---

## Riferimenti

- Hugging Face Transformers: https://huggingface.co/transformers/  
- MLflow Documentation: https://mlflow.org/docs/latest/index.html  
- Evidently AI: https://github.com/evidentlyai/evidently  
- FastAPI: https://fastapi.tiangolo.com/