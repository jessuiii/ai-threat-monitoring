import pandas as pd
import joblib

from quantum_module import quantum_risk_score

# Load trained RF model
rf = joblib.load("rf_ids_model.pkl")

# Load sample data
df = pd.read_csv("unsw_demo.csv").sample(5, random_state=42)

X = df.drop("label", axis=1)

# Classical RF probabilities
rf_probs = rf.predict_proba(X)[:, 1]

print("\n--- HYBRID IDS OUTPUT ---\n")

for i, row in X.iterrows():
    classical_prob = rf_probs[list(X.index).index(i)]

    # Use 2 features for quantum encoding
    q_score = quantum_risk_score([
        row["rate"],
        row["spkts"]
    ])

    # Hybrid fusion
    final_risk = 0.7 * classical_prob + 0.3 * q_score

    print(f"Classical RF Risk : {classical_prob:.3f}")
    print(f"Quantum Risk     : {q_score:.3f}")
    print(f"Final Hybrid Risk: {final_risk:.3f}")

    if final_risk > 0.6:
        print("🚨 ALERT: High‑Risk Traffic\n")
    else:
        print("✅ Normal Traffic\n")
