import os
import mlflow
import mlflow.pytorch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import evaluate
import numpy as np
from dotenv import load_dotenv
import torch
from pathlib import Path
from huggingface_hub.repocard import RepoCard

# === Carica variabili d'ambiente ===
load_dotenv()

root_path = Path(__file__).parent.parent

MODEL_NAME = os.getenv("MODEL_NAME", "cardiffnlp/twitter-roberta-base-sentiment-latest")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")
MLFLOW_EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT", "sentiment-pipeline")
TRAIN_MODE = os.getenv("TRAIN_MODE", "pretrained")  # "fine_tune" oppure "pretrained"

mlflow.set_tracking_uri(root_path / MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT)

# === Funzioni di supporto ===
def preprocess_function(examples, tokenizer):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = (preds == labels).mean()
    f1 = evaluate.load("f1")
    f1score = f1.compute(predictions=preds, references=labels, average="weighted")["f1"]
    return {"accuracy": float(acc), "f1": float(f1score)}

def get_device():
    """Restituisce 'cuda' se disponibile, altrimenti 'cpu'."""
    return "cuda" if torch.cuda.is_available() else "cpu"

def create_model_card(output_dir: Path, model_name: str, train_mode: str):
    """Genera automaticamente un README.md compatibile con Hugging Face e verifica la validità."""
    readme_path = output_dir / "README.md"

    content = f"""---
language: it
license: apache-2.0
tags:
  - sentiment-analysis
  - roberta
  - twitter
  - mlflow
pipeline_tag: text-classification
widget:
  - text: "Oggi è una splendida giornata!"
  - text: "Questo prodotto fa davvero schifo..."
---

# Modello di Sentiment Analysis

Questo modello utilizza la base **{model_name}** ed è stato generato in modalità **{train_mode}**.  
Classifica i testi in tre categorie: **positivo**, **neutro** e **negativo**.

## Dettagli tecnici
- Architettura: RoBERTa-base
- Dataset: tweet_eval/sentiment
- Librerie: Hugging Face Transformers, MLflow
- Device di training: {get_device()}

## Output
Il modello e il tokenizer sono salvati nella directory:
`{output_dir}`
"""

    # Scrivi senza BOM e assicurati che non ci siano spazi o CRLF extra
    with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.strip() + "\n")

    print(f"README.md creato in {readme_path}")

    # Verifica la validità
    try:
        card = RepoCard.load(str(readme_path))
        if card.data:
            print("Metadata YAML validi e riconosciuti da Hugging Face:")
            print(card.data)
        else:
            print("YAML non riconosciuto: controlla che il file inizi con '---'")
    except Exception as e:
        print(f"Errore nel parsing del README: {e}")

from huggingface_hub.repocard import RepoCard

def sanitize_and_validate_readme(readme_path: str):
    """Rimuove BOM, righe vuote e verifica validità YAML del README.md"""
    with open(readme_path, "r", encoding="utf-8-sig") as f:  # utf-8-sig rimuove BOM
        content = f.read().strip()

    # Forza newline Unix e nessuna riga vuota
    lines = [line.strip("\r") for line in content.splitlines()]
    cleaned = "\n".join(lines).strip() + "\n"

    with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(cleaned)

    print(f"README.md sanificato: {readme_path}")

    try:
        card = RepoCard.load(readme_path)
        if card.data:
            print("YAML riconosciuto da Hugging Face:")
            print(card.data)
        else:
            print("YAML non riconosciuto — verifica che inizi esattamente con ---")
    except Exception as e:
        print(f"Errore nel parsing del README: {e}")

# === MAIN ===
def main():
    print("Avvio pipeline Sentiment Analysis")
    print(f"Modalità: {TRAIN_MODE}")
    print(f"Modello base: {MODEL_NAME}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"MLflow URI: {MLFLOW_TRACKING_URI}")
    print(f"Device: {get_device()}")

    for k in ("HF_TOKEN", "HUGGINGFACE_HUB_TOKEN", "HUGGINGFACE_TOKEN"):
        os.environ.pop(k, None)

    dataset = load_dataset("tweet_eval", "sentiment", token=None)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenized = dataset.map(lambda x: preprocess_function(x, tokenizer), batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3).to(get_device())

    with mlflow.start_run(run_name=TRAIN_MODE):
        mlflow.log_param("base_model", MODEL_NAME)
        mlflow.log_param("train_mode", TRAIN_MODE)

        # === TRAINING ===
        if TRAIN_MODE.lower() == "fine_tune":
            print("Modalità training attiva — avvio fine-tuning...")
            training_args = TrainingArguments(
                output_dir=OUTPUT_DIR,
                overwrite_output_dir=True,
                eval_strategy="epoch",
                save_strategy="epoch",
                per_device_train_batch_size=16,
                per_device_eval_batch_size=32,
                num_train_epochs=2,
                logging_steps=100,
                load_best_model_at_end=True,
                metric_for_best_model="accuracy",
                report_to="none",
            )

            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=tokenized["train"],
                eval_dataset=tokenized["validation"],
                tokenizer=tokenizer,
                compute_metrics=compute_metrics
            )

            trainer.train()
            eval_res = trainer.evaluate()
            for k, v in eval_res.items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))

            trainer.save_model(OUTPUT_DIR)
            mlflow.pytorch.log_model(trainer.model, name="model")
            tokenizer.save_pretrained(os.path.join(OUTPUT_DIR, "tokenizer"))

            # Crea automaticamente la card
            create_model_card(Path(OUTPUT_DIR), MODEL_NAME, TRAIN_MODE)

            sanitize_and_validate_readme(str(Path(OUTPUT_DIR) / "README.md"))

            print("Training completato. Artefatti salvati in outputs/ e su MLflow.")

        # === SOLO MODELLO PRETRAINED ===
        else:
            print("Modalità pretrained: salto la fase di training.")
            pretrained_path = root_path / OUTPUT_DIR / "model_pretrained"
            pretrained_path.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(pretrained_path)
            tokenizer.save_pretrained(pretrained_path)
            mlflow.pytorch.log_model(model, name="model_pretrained")

            # Anche qui, crea la card
            create_model_card(pretrained_path, MODEL_NAME, TRAIN_MODE)

            print("Modello pre-addestrato salvato senza training.")

    print("Pipeline completata.")


if __name__ == "__main__":
    main()