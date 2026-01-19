import joblib
import pandas as pd
from preprocess import preprocess

bundle = joblib.load("ml/rf_ids_model.pkl")

rf_model = bundle["model"]
FEATURES = bundle["features"]
encoders = bundle["encoders"]
scaler = bundle["scaler"]

df = pd.read_csv("dataset/raw/test.csv")

# Apply SAME preprocessing (fit=False)
X, _ = preprocess(df, fit=False, encoders=encoders, scaler=scaler)

# Enforce same feature order
X = X[FEATURES]

preds = rf_model.predict(X.head(5))
print("Predictions:", preds)
