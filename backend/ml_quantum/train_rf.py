# ml_quantum/train_rf.py
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from ml_quantum.preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "..", "dataset", "raw", "train.csv")
MODEL_PATH = os.path.join(BASE_DIR, "rf_ids_model.pkl")

print("📂 Loading dataset from:", DATASET_PATH)
df = pd.read_csv(DATASET_PATH)

# -------------------------------
# REQUIRED TARGET
# -------------------------------
if "attack_cat" not in df.columns:
    raise ValueError("❌ attack_cat column missing")

# Optional feature
if "burst_rate" not in df.columns:
    df["burst_rate"] = 0.0

print("Dataset shape:", df.shape)
print("Attack distribution:\n", df["attack_cat"].value_counts())

# -------------------------------
# TRAIN
# -------------------------------
X, y, encoders, scaler, FEATURES = preprocess(df, fit=True)

rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=30,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("🚀 Training multi-class Random Forest...")
rf.fit(X, y)

bundle = {
    "model": rf,
    "features": FEATURES,
    "encoders": encoders,
    "scaler": scaler,
    "classes": rf.classes_,   # 🔥 CRITICAL
}

joblib.dump(bundle, MODEL_PATH, protocol=4)
print("✅ Multi-class model saved:", MODEL_PATH)
print("Classes learned:", rf.classes_)
