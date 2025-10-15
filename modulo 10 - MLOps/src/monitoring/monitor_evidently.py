import os
import json
import time
import argparse
import pandas as pd
from dotenv import load_dotenv
from datasets import load_dataset
from pathlib import Path
from evidently import Report
from evidently.presets import DataDriftPreset

load_dotenv()

LOGS_PATH = os.getenv("INFERENCE_LOGS_PATH", "logs/inference_logs.parquet")
OUTPUT_DIR = os.getenv("MONITOR_OUTPUT_DIR", "monitor_reports")
REF_DATASET = os.getenv("REF_DATASET", "tweet_eval")
REF_CONFIG = os.getenv("REF_CONFIG", "sentiment")
REF_SPLIT = os.getenv("REF_SPLIT", "validation")

root_path = Path(__file__).parent.parent.parent

os.makedirs(root_path / "outputs" / OUTPUT_DIR, exist_ok=True)


def _parse_pred_cell(cell):
    """Estrae (label, label_idx) da cella con JSON o dict di predizione."""
    if pd.isna(cell):
        return None, None
    try:
        if isinstance(cell, dict):
            return cell.get("label"), cell.get("label_idx")
        if isinstance(cell, str):
            try:
                parsed = json.loads(cell)
                if isinstance(parsed, dict):
                    return parsed.get("label"), parsed.get("label_idx")
            except Exception:
                return cell, None
        if isinstance(cell, (int, float)):
            return None, int(cell)
    except Exception:
        pass
    return str(cell), None


def load_reference():
    """Carica il dataset di riferimento da Hugging Face (tweet_eval/sentiment)."""
    try:
        ds = load_dataset(REF_DATASET, REF_CONFIG, split=REF_SPLIT)
        df = pd.DataFrame({"text": ds["text"], "target": ds["label"]})
        print(f"[INFO] Reference dataset caricato: {len(df)} righe.")
        return df
    except Exception as e:
        print(f"[WARN] Errore nel caricamento del dataset di riferimento: {e}")
        return pd.DataFrame(columns=["text", "target"])


def load_current():
    """Carica i log correnti da file Parquet (prodotti dall’inferenza)."""
    if not os.path.exists(root_path / LOGS_PATH):
        print(f"[WARN] File log non trovato: {LOGS_PATH}")
        return pd.DataFrame(columns=["text", "prediction", "prediction_label_idx"])

    df = pd.read_parquet(root_path / LOGS_PATH)
    if df.empty:
        print(f"[WARN] File Parquet vuoto: {LOGS_PATH}")
        return pd.DataFrame(columns=["text", "prediction", "prediction_label_idx"])

    # trova colonna testuale
    text_cols = [c for c in df.columns if "text" in c.lower()]
    text_col = text_cols[0] if text_cols else df.columns[0]

    # trova colonna predizione
    pred_cols = [c for c in df.columns if "prediction" in c.lower()]
    pred_col = pred_cols[0] if pred_cols else None

    result = pd.DataFrame()
    result["text"] = df[text_col].astype(str)

    if pred_col:
        parsed = df[pred_col].apply(lambda v: _parse_pred_cell(v))
        result["prediction"] = parsed.apply(lambda t: t[0])
        result["prediction_label_idx"] = parsed.apply(lambda t: t[1])
    elif "label" in df.columns:
        result["prediction"] = df["label"].astype(str)
    if "prediction_label_idx" in result.columns:
        result = result.rename(columns={"prediction_label_idx": "target"})

    print(f"[INFO] Log corrente caricato: {len(result)} righe.")
    return result


def build_report(reference_df, current_df, output_dir=OUTPUT_DIR):
    """Genera e salva un report Evidently (solo DataDrift) in modo robusto."""
    # Normalizza le colonne in modo che entrambi i DF abbiano le stesse
    # Evidently si aspetta lo stesso schema per reference e current
    common_cols = list(set(reference_df.columns) & set(current_df.columns))
    if not common_cols:
        raise ValueError(f"Nessuna colonna comune trovata tra reference e current: "
                         f"{reference_df.columns} vs {current_df.columns}")

    reference_df = reference_df[common_cols].copy()
    current_df = current_df[common_cols].copy()

    # Rimuovi eventuali righe con NaN, che causano errori nel drift test
    reference_df = reference_df.dropna().reset_index(drop=True)
    current_df = current_df.dropna().reset_index(drop=True)

    # Log di controllo
    print(f"[INFO] Colonne usate per il drift report: {common_cols}")
    print(f"[INFO] Reference shape: {reference_df.shape}, Current shape: {current_df.shape}")

    # Esegui il report Evidently
    report = Report(metrics=[DataDriftPreset()])
    try:
        result_report = report.run(reference_data=reference_df, current_data=current_df)
    except Exception as e:
        print(f"[ERROR] Errore in Evidently report.run: {e}")
        raise

    ts = int(time.time())
    html_path = root_path / "outputs" / output_dir / f"evidently_report_{ts}.html"
    result_report.save_html(str(html_path))
    print(f"[INFO] Report Evidently salvato in {html_path}")
    return html_path


def main():
    parser = argparse.ArgumentParser(description="Genera un report Evidently da log inferenza")
    parser.add_argument("--logs", type=str, default=LOGS_PATH, help="Percorso file log Parquet")
    parser.add_argument("--out", type=str, default=OUTPUT_DIR, help="Cartella output report")
    args = parser.parse_args()

    ref = load_reference()
    cur = load_current()

    if cur.empty:
        print("[WARN] Nessun log corrente trovato. Esco.")
        return

    build_report(ref, cur, output_dir=OUTPUT_DIR)


if __name__ == "__main__":
    main()