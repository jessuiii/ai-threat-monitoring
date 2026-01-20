import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from preprocess import preprocess

# 1️⃣ Load FULL training dataset
df = pd.read_csv("dataset/raw/train.csv")

print(f"Dataset shape: {df.shape}")

# 2️⃣ Preprocess (FIT MODE)
X, y, encoders, scaler, FEATURES = preprocess(df, fit=True)

print(f"Training features: {len(FEATURES)}")

# 3️⃣ Initialize Random Forest
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

# 4️⃣ Train model on FULL data
rf.fit(X, y)

# 5️⃣ Save EVERYTHING needed for inference
joblib.dump(
    {
        "model": rf,
        "features": FEATURES,
        "encoders": encoders,
        "scaler": scaler
    },
    "ml/rf_ids_model.pkl"
)

print("✅ Random Forest trained on FULL dataset and saved")
