# ml_quantum/preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess(df, *, fit: bool, encoders=None, scaler=None, features=None):
    df = df.copy()

    # Drop non-feature columns
    df.drop(columns=["id"], errors="ignore", inplace=True)

    # ===============================
    # TRAINING MODE
    # ===============================
    if fit:
        if "attack_cat" not in df.columns:
            raise ValueError("Training data must include 'attack_cat'")

        y = df["attack_cat"]
        X = df.drop(columns=["attack_cat"])

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

        # Ensure feature consistency
        for col in features:
            if col not in X.columns:
                X[col] = 0.0

        X = X[features]

        for col, le in encoders.items():
            if col in X.columns:
                X[col] = X[col].astype(str).apply(
                    lambda x: le.transform([x])[0]
                    if x in le.classes_
                    else -1
                )

        X[X.columns] = scaler.transform(X)
        return X
