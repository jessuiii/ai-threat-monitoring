# ml_quantum/classical_inference.py
import os
import joblib
import pandas as pd
from ml_quantum.preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "rf_ids_model.pkl")

_bundle = None

def load_model():
    global _bundle
    if _bundle is None:
        _bundle = joblib.load(MODEL_PATH)
    return _bundle

def classical_risk(df: pd.DataFrame):
    bundle = load_model()
    df = df.copy()

    # 🔥 Option A: burst_rate must exist
    if "burst_rate" not in df.columns:
        df["burst_rate"] = 0.0

    X = preprocess(
        df,
        fit=False,
        encoders=bundle["encoders"],
        scaler=bundle["scaler"],
        features=bundle["features"],
    )

    return bundle["model"].predict_proba(X)[:, 1]
