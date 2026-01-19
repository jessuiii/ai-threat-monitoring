import pandas as pd
from hybrid_ids import hybrid_decision
from alert_logic import classify_risk

# Load FULL test dataset
df = pd.read_csv("dataset/raw/test.csv")

# Run hybrid inference
classical, quantum, final = hybrid_decision(df)
alerts = classify_risk(final)

# Attach results
df["classical_risk"] = classical
df["quantum_risk"] = quantum
df["final_risk"] = final
df["alert"] = alerts

# Save results for inspection / reporting
df.to_csv("outputs/hybrid_inference_results.csv", index=False)

print("✅ Hybrid inference completed on full test dataset")
print(df["alert"].value_counts())
