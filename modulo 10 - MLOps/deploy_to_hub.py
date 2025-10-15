"""
Script completo:
1 Carica modello e tokenizer su Hugging Face Hub
2 Crea/aggiorna la model card
3️ Crea automaticamente uno Space Gradio per testare il modello
"""

import os
import json
from dotenv import load_dotenv
from huggingface_hub import HfApi, HfFolder, login
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# === Config ===
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_USERNAME = os.getenv("HF_USERNAME")
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "sentiment-model")
HF_SPACE_NAME = os.getenv("HF_SPACE_NAME", "sentiment-space")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs/model_pretrained")

if not HF_TOKEN or not HF_USERNAME:
    raise ValueError("Devi specificare HF_TOKEN e HF_USERNAME nel file .env")

repo_id = f"{HF_USERNAME}/{HF_MODEL_REPO}"
space_id = f"{HF_USERNAME}/{HF_SPACE_NAME}"

# === Login ===
print(f"Login su Hugging Face come {HF_USERNAME} ...")
login(token=HF_TOKEN)
HfFolder.save_token(HF_TOKEN)
api = HfApi()

# === Crea/aggiorna repo modello ===
print(f"Creazione o aggiornamento del repo modello '{repo_id}' ...")
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# === Caricamento modello e tokenizer ===
print("Caricamento modello e tokenizer su Hugging Face Hub ...")
model = AutoModelForSequenceClassification.from_pretrained(OUTPUT_DIR)
tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR)

model.push_to_hub(repo_id)
tokenizer.push_to_hub(repo_id)

# === Crea/aggiorna README.md ===
readme_path = os.path.join(OUTPUT_DIR, "README.md")
if not os.path.exists(readme_path):
    print("Creazione file README.md ...")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"""
        ---
        language: it
        license: mit
        tags:
        - sentiment-analysis
        - roberta
        - twitter
        pipeline_tag: text-classification
        ---

        # {HF_MODEL_REPO}
        
        Questo modello è una versione fine-tuned di 
        [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
        addestrata per sentiment analysis (positivo, neutro, negativo).
        
        ## Esempio di utilizzo
        
        ```python
        from transformers import pipeline
        pipe = pipeline("text-classification", model="{repo_id}")
        print(pipe("Questo film è fantastico!"))
        """)

api.upload_file(
    path_or_fileobj=readme_path,
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="model",
)

print(f"Modello caricato su: https://huggingface.co/{repo_id}")

# === Crea/aggiorna Space Gradio ===

print("Creazione/aggiornamento dello Space Gradio...")

## Cartella locale temporanea per lo Space

space_dir = "space_app"
os.makedirs(space_dir, exist_ok=True)

## app.py per Gradio

with open(os.path.join(space_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(f"""
    import gradio as gr
    
    from transformers import pipeline
    
    pipe = pipeline("text-classification", model="{repo_id}")
    
    def predict_sentiment(text):
    result = pipe(text)[0]
    return f"Predizione: {{result['label']}} (score: {{result['score']:.2f}})"
    
    demo = gr.Interface(
        fn=predict_sentiment,
        inputs=gr.Textbox(lines=3, label="Testo da analizzare"),
        outputs=gr.Textbox(label="Risultato"),
        title="Twitter Sentiment Analysis",
        description="Modello basato su {repo_id} per classificare sentiment positivo, neutro o negativo."
    )
    
    if name == "main":
    demo.launch()
    """)

# requirements.txt per lo Space

with open(os.path.join(space_dir, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write("transformers\ngradiio\ntorch\n")

# README.md per lo Space

with open(os.path.join(space_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(f"# {HF_SPACE_NAME}\n\nInterfaccia Gradio per testare il modello {repo_id}.")

# Crea o aggiorna lo Space

api.create_repo(repo_id=space_id, repo_type="space", exist_ok=True, space_sdk="gradio")

# Carica i file nello Space

api.upload_folder(
    folder_path=space_dir,
    repo_id=space_id,
    repo_type="space",
    path_in_repo="."
)

print(f"Space creato su: https://huggingface.co/spaces/{space_id}")

