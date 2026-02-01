# ml_quantum/train_rf.py
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif
try:
    from backend.ml_quantum.preprocess import preprocess
except ImportError:
    # Ensure local import works when running directly
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from backend.ml_quantum.preprocess import preprocess

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

# Use 'x' and 'y' correctly
y = df["attack_cat"]
# DROP TARGETS AND NON-FEATURES
# 'label' is the binary target (0/1), 'id' is identifier
drop_cols = ["attack_cat", "label", "id", "Label"]
X_full = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Optional feature
if "burst_rate" not in df.columns:
    df["burst_rate"] = 0.0

print("Dataset shape:", df.shape)
print("Attack distribution:\n", df["attack_cat"].value_counts())

# -------------------------------
# TRAIN
# -------------------------------
# 1. Preprocess (Encode + Scale)
# We manually handle X and y above, so we pass X_full to preprocess
# BUT preprocess expects a DF and splits it if fit=True. 
# Let's fix preprocess usage or just pass the clean DF.

# Re-reading: preprocess(df, fit=True) does: y = df["attack_cat"], X = df.drop("attack_cat")
# We already dropped targets from df if we pass it, but X_full is derived from df.drop
# Preprocess splits df. Let's make sure df itself is clean or just use X_full logic.
# Actually, preprocess(df) expects df to have attack_cat to split y.
# So we should pass df with attack_cat BUT without label/id.

# CRITICAL FIX: Ensure 'label' and 'id' are removed from the df passed to preprocess
for col in ["label", "Label", "id"]:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

X_full, y, encoders, scaler, all_features = preprocess(df, fit=True)

# 2. Feature Selection (Mutual Information)
print("🔍 Performing Feature Selection (Mutual Information)...")
# Select top 20 features (adjust k as needed based on performance/latency trade-off)
selector = SelectKBest(score_func=mutual_info_classif, k=20)
X_selected = selector.fit_transform(X_full, y)

# Get selected feature names
selected_mask = selector.get_support()
selected_features = [f for f, selected in zip(all_features, selected_mask) if selected]
print(f"✅ Selected {len(selected_features)} features: {selected_features}")

# 3. Train Random Forest
rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=30,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("🚀 Training multi-class Random Forest on selected features...")
rf.fit(X_selected, y)

bundle = {
    "model": rf,
    "features": all_features,          # For Preprocess/Scaling (Must match scaler)
    "selected_features": selected_features, # For Model Prediction (Subset)
    "encoders": encoders,
    "scaler": scaler,
    "classes": rf.classes_,
}

joblib.dump(bundle, MODEL_PATH, protocol=4)
print("✅ Multi-class model saved with", len(selected_features), "selected features.")
print("Classes learned:", rf.classes_)
