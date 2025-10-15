# Model Card — Sentiment Model 

## Nome modello
cardiffnlp/twitter-roberta-base-sentiment-latest (usato come base)

## Descrizione
Modello RoBERTa base fine-tuned per sentiment analysis su tweet (TweetEval). Labels: 0 negative, 1 neutral, 2 positive. Fonte: Hugging Face model page. :contentReference[oaicite:1]{index=1}

## Dataset di training
- Ticket: TweetEval (tweet) e dataset aggregati usati dal modello di base (vedere model card originale).

## Metriche (esempio)
- accuracy (validation): X.XX
- f1 (weighted): X.XX

(Compilare con metriche usate da MLflow dopo training)

## Limitazioni e bias
- Addestrato su tweet in inglese (periodo 2018–2021). Potrebbe non generalizzare ad altre lingue o a linguaggio fuorviante.
- Potenziali bias verso espressioni culturali relative al periodo di training.

## Uso
- Endpoint: `/predict` (FastAPI) che ritorna: label, label_idx, probs, timestamp.
- Esempio:
```json
{"label":"positive","label_idx":2,"probs":[0.01,0.02,0.97],"timestamp":...}