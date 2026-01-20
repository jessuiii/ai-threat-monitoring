import os
import joblib
from ml_quantum.preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "rf_ids_model.pkl"   # ✅ model is in ml_quantum/
)

_bundle = None

def load_model():
    global _bundle
    if _bundle is None:
        _bundle = joblib.load(MODEL_PATH)
    return _bundle


def classical_risk(df):
    bundle = load_model()

    rf_model = bundle["model"]
    FEATURES = bundle["features"]
    encoders = bundle["encoders"]
    scaler = bundle["scaler"]

    X, _ = preprocess(df, fit=False, encoders=encoders, scaler=scaler)
    X = X[FEATURES]

    return rf_model.predict_proba(X)[:, 1]
