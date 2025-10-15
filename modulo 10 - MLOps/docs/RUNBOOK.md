```markdown
# Runbook operativo (Sintesi)

## Deploy
- Workflow GitHub: `train_and_publish.yaml` pubblica artifacts su HF Hub (repo definito in HF_REPO_ID).
- Per deploy su HF Inference: creare model repo e abilitare Inference (dashboard HF).

## Rollback
- Se deploy introduce degradazione, rollback al commit precedente e alla versione del modello su HF Hub (tag o versione nel repo).

## Alerting
- Soglie consigliate:
  - Drop accuracy > 5% rispetto baseline → alert
  - % predizioni con confidenza < 0.6 > 20% → alert
  - Drift embedding (cosine shift) > 0.1 → alert

## Troubleshooting
- Errori token HF: verificare secret HF_TOKEN.
- MLflow: controllare `MLFLOW_TRACKING_URI`.