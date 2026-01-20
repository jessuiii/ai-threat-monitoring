import joblib
from ml_quantum.preprocess import preprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "rf_ids_model.pkl"
)

bundle = joblib.load(MODEL_PATH)

rf_model = bundle["model"]
FEATURES = bundle["features"]
encoders = bundle["encoders"]
scaler = bundle["scaler"]

def classical_risk(df):
    X, _ = preprocess(df, fit=False, encoders=encoders, scaler=scaler)
    X = X[FEATURES]

    # Probability of attack (class = 1)
    probs = rf_model.predict_proba(X)[:, 1]
    return probs
