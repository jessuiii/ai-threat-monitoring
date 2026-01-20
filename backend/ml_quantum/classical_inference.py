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

def predict_attack(df: pd.DataFrame):
    bundle = load_model()
    df = df.copy()

    if "burst_rate" not in df.columns:
        df["burst_rate"] = 0.0

    X = preprocess(
        df,
        fit=False,
        encoders=bundle["encoders"],
        scaler=bundle["scaler"],
        features=bundle["features"],
    )

    probs = bundle["model"].predict_proba(X)[0]
    classes = bundle["classes"]

    result = dict(zip(classes, probs))

    predicted_attack = classes[probs.argmax()]
    confidence = probs.max()

    return {
        "attack_type": predicted_attack,
        "confidence": float(confidence),
        "distribution": result
    }
