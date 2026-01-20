import pandas as pd
from ml_quantum.hybrid_ids import hybrid_decision
from ml_quantum.alert_logic import classify_risk

def predict_event(event: dict):
    """
    Run ML + quantum inference on a single event
    """

    df = pd.DataFrame([event])

    classical, quantum, final = hybrid_decision(df)
    label = classify_risk(final)[0]

    return {
        "label": label,
        "confidence": float(classical[0]),
        "threat_distance": float(1.0 - final[0])
    }
