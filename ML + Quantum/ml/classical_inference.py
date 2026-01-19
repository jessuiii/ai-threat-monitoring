import joblib
from preprocess import preprocess

bundle = joblib.load("ml/rf_ids_model.pkl")

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
