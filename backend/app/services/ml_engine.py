# backend/app/services/ml_engine.py

import pandas as pd
from ml_quantum.hybrid_ids import hybrid_decision


def predict_event(event: dict, key: str):
    """
    Runs hybrid ML + quantum + memory inference
    and returns API-safe response.
    """

    # Convert event to DataFrame
    df = pd.DataFrame([event])

    # Hybrid inference
    result = hybrid_decision(df, key=key)

    attack_type = result["attack_type"]
    final_risk = result["final_risk"]
    confidence = result["confidence"]

    # Threat distance = divergence indicator
    threat_distance = abs(final_risk - confidence)

    return {
        "attack_type": attack_type,
        "confidence": float(confidence),
        "threat_distance": float(threat_distance),
    }
