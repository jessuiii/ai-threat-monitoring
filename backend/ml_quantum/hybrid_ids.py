# ml_quantum/hybrid_ids.py

from ml_quantum.classical_inference import classical_risk
from ml_quantum.quantum_module import adaptive_quantum_risk
from app.services.threat_memory import get_or_create_state, update_state


def hybrid_decision(df, key: str, alpha: float = 0.6):
    """
    Hybrid decision engine:
    - Multi-class classical ML (what attack?)
    - Quantum-inspired adaptation (how confident over time?)
    - Persistent threat memory (does this source repeat?)
    """

    # --------------------------------------
    # 1. Classical ML (multi-class)
    # --------------------------------------
    classical_output = classical_risk(df)

    attack_type = classical_output["attack_type"]
    confidence = float(classical_output["confidence"])  # max class probability

    # --------------------------------------
    # 2. Load persistent threat memory
    # --------------------------------------
    state = get_or_create_state(key)

    # --------------------------------------
    # 3. Quantum-inspired risk adaptation
    # --------------------------------------
    quantum_risk = adaptive_quantum_risk(
        confidence,
        {
            "recurrence": state.recurrence,
            "confidence_drift": abs(state.risk_score - confidence)
        }
    )

    # --------------------------------------
    # 4. Escalation logic (memory-based)
    # --------------------------------------
    escalation = min(state.recurrence * 0.15, 0.6)

    final_risk = (
        alpha * confidence
        + (1 - alpha) * quantum_risk
        + escalation
    )

    final_risk = min(final_risk, 1.0)

    # --------------------------------------
    # 5. Persist updated threat state
    # --------------------------------------
    update_state(key, final_risk)

    # --------------------------------------
    # 6. Return structured decision
    # --------------------------------------
    return {
        "attack_type": attack_type,
        "final_risk": float(final_risk),
        "confidence": confidence,
        "quantum_risk": float(quantum_risk),
        "recurrence": state.recurrence + 1
    }
