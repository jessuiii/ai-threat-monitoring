import pandas as pd
import joblib

rf = joblib.load("rf_ids_model.pkl")

df = pd.read_csv("unsw_demo.csv").sample(5)

X = df.drop("label", axis=1)

probs = rf.predict_proba(X)[:, 1]

for i, p in enumerate(probs):
    print(f"Sample {i} → Attack Probability: {round(p, 3)}")
