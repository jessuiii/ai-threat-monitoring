import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess(df, fit=True, encoders=None, scaler=None):
    df = df.drop(columns=['id', 'attack_cat'], errors='ignore')

    y = df['label']
    X = df.drop(columns=['label'])

    FEATURES = X.columns.tolist()

    if fit:
        encoders = {}
        for col in X.select_dtypes(include='object').columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

        scaler = StandardScaler()
        X[X.columns] = scaler.fit_transform(X)

        return X, y, encoders, scaler, FEATURES

    else:
        for col, le in encoders.items():
            # ✅ handle unseen labels safely
            X[col] = X[col].astype(str).apply(
                lambda x: le.transform([x])[0] if x in le.classes_ else -1
            )

        X[X.columns] = scaler.transform(X)
        return X, y
