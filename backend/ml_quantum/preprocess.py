import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ======================================================
# Unified Preprocessing for TRAINING and INFERENCE
# ======================================================
def preprocess(df, *, fit: bool, encoders=None, scaler=None, features=None):
    df = df.copy()

    # Drop non-feature columns safely
    df.drop(columns=["id", "attack_cat"], errors="ignore", inplace=True)

    # ===============================
    # TRAINING MODE
    # ===============================
    if fit:
        if "label" not in df.columns:
            raise ValueError("Training data must include 'label' column")

        y = df["label"]
        X = df.drop(columns=["label"])

        encoders = {}
        for col in X.select_dtypes(include="object").columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

        scaler = StandardScaler()
        X[X.columns] = scaler.fit_transform(X)

        features = X.columns.tolist()

        return X, y, encoders, scaler, features

    # ===============================
    # INFERENCE MODE
    # ===============================
    else:
        X = df

        # Add missing features
        for col in features:
            if col not in X.columns:
                X[col] = 0.0

        X = X[features]

        # Encode categorical
        for col, le in encoders.items():
            if col in X.columns:
                X[col] = X[col].astype(str).apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )

        X[X.columns] = scaler.transform(X)
        return X
