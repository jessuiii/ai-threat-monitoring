import pandas as pd
from ml_quantum.hybrid_ids import hybrid_decision

def predict_event(event: dict, key: str):
    df = pd.DataFrame([event])

    result = hybrid_decision(df, key=key)

    return {
        "attack_type": result["attack_type"],
        "confidence": float(result["confidence"]),
        "threat_distance": abs(
            float(result["final_risk"]) - float(result["confidence"])
        ),
    }
