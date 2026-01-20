import pandas as pd
from ml_quantum.hybrid_ids import hybrid_decision
from ml_quantum.alert_logic import classify_risk

def predict_event(event: dict, key: str):
    df = pd.DataFrame([event])

    classical, quantum, final = hybrid_decision(df, key=key)

    label = classify_risk([final])[0]

    return {
        "label": label,
        "confidence": float(classical),
        "threat_distance": float(abs(classical - final))
    }
