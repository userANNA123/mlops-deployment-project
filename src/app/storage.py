from pathlib import Path
import pandas as pd
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent / "prod_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = DATA_DIR / "predictions.csv"

def save_prediction_to_csv(payload: dict, prediction: int) -> None:
    row = dict(payload)
    row["prediction"] = int(prediction)
    row["timestamp"] = datetime.utcnow().isoformat()

    df = pd.DataFrame([row])
    if CSV_PATH.exists():
        df.to_csv(CSV_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)
