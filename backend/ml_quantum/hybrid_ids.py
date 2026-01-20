from ml_quantum.classical_inference import classical_risk
from ml_quantum.quantum_module import adaptive_quantum_risk
from app.services.threat_memory import get_or_create_state, update_state

def hybrid_decision(df, key, alpha=0.6):
    classical = classical_risk(df)[0]

    state = get_or_create_state(key)

    quantum = adaptive_quantum_risk(
        classical,
        {
            "recurrence": state.recurrence,
            "confidence_drift": abs(state.risk_score - classical)
        }
    )

    escalation = min(state.recurrence * 0.15, 0.6)

    final = alpha * classical + (1 - alpha) * quantum + escalation
    final = min(final, 1.0)

    update_state(key, final)

    return classical, quantum, final
