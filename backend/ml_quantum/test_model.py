import joblib
import os
import pandas as pd
from ml_quantum.preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "rf_ids_model.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "..", "..", "dataset", "raw", "test.csv")

bundle = joblib.load(MODEL_PATH)

rf_model = bundle["model"]
FEATURES = bundle["features"]
encoders = bundle["encoders"]
scaler = bundle["scaler"]

df = pd.read_csv(DATASET_PATH)

X, _ = preprocess(df, fit=False, encoders=encoders, scaler=scaler)
X = X[FEATURES]

preds = rf_model.predict(X.head(5))
print("Predictions:", preds)
