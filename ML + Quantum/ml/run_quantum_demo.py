import pandas as pd
from hybrid_ids import hybrid_decision
from alert_logic import classify_risk

# Load test samples
df = pd.read_csv("dataset/raw/test.csv").head(5)

classical, quantum, final = hybrid_decision(df)
labels = classify_risk(final)

for i in range(len(df)):
    print("\n--- HYBRID IDS OUTPUT ---")
    print(f"Classical Risk : {classical[i]:.4f}")
    print(f"Quantum Risk   : {quantum[i]:.4f}")
    print(f"Final Risk     : {final[i]:.4f}")
    print(f"Decision       : {labels[i]}")
