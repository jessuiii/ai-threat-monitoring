import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR, "..", "..", "dataset", "raw", "train.csv"
)

MODEL_PATH = os.path.join(BASE_DIR, "rf_ids_model.pkl")

print("📂 Loading dataset from:", DATASET_PATH)
df = pd.read_csv(DATASET_PATH)

# Option A feature
if "burst_rate" not in df.columns:
    df["burst_rate"] = 0.0

print("Dataset shape:", df.shape)

# ===============================
# TRAIN
# ===============================
X, y, encoders, scaler, FEATURES = preprocess(df, fit=True)

print("Number of features:", len(FEATURES))
print("Features:", FEATURES)

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("🚀 Training Random Forest...")
rf.fit(X, y)

bundle = {
    "model": rf,
    "features": FEATURES,
    "encoders": encoders,
    "scaler": scaler
}

joblib.dump(bundle, MODEL_PATH, protocol=4)
print("✅ Model retrained and saved to:", MODEL_PATH)
