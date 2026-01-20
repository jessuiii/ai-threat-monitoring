# ml_quantum/hybrid_ids.py
from ml_quantum.classical_inference import predict_attack
from ml_quantum.quantum_module import adaptive_quantum_risk
from app.services.threat_memory import get_or_create_state, update_state


def hybrid_decision(df, key: str, alpha: float = 0.6):
    classical = predict_attack(df)

    attack_type = classical["attack_type"]
    confidence = classical["confidence"]

    state = get_or_create_state(key)

    quantum_risk = adaptive_quantum_risk(
        confidence,
        {
            "recurrence": state.recurrence,
            "confidence_drift": abs(state.risk_score - confidence),
        }
    )

    escalation = min(state.recurrence * 0.15, 0.6)

    final_risk = min(
        alpha * confidence + (1 - alpha) * quantum_risk + escalation,
        1.0,
    )

    update_state(key, final_risk)

    return {
        "attack_type": attack_type,
        "final_risk": final_risk,
        "confidence": confidence,
        "quantum_risk": quantum_risk,
        "recurrence": state.recurrence + 1,
    }
