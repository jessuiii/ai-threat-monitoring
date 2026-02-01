# ml_quantum/hybrid_ids.py
import logging
try:
    from backend.ml_quantum.classical_inference import predict_attack
    from backend.ml_quantum.quantum_module import calculate_quantum_risk
    from backend.ml_quantum.threat_memory import ThreatMemory
except ImportError:
    from ml_quantum.classical_inference import predict_attack
    from ml_quantum.quantum_module import calculate_quantum_risk
    from ml_quantum.threat_memory import ThreatMemory

# Initialize Singleton Memory
memory_store = ThreatMemory()

def hybrid_decision(df, key: str):
    # 1. Classical Prediction
    classical = predict_attack(df)
    
    attack_type = classical["attack_type"]
    confidence = classical["confidence"]
    distribution = classical["distribution"]
    
    # Extract Probabilities
    # Check for 'Normal' or 'normal' or 0
    prob_normal = distribution.get("Normal", distribution.get("normal", 0.0))
    
    # Probability of Attack = 1 - Prob(Normal)
    # Or max probability of any attack class
    prob_attack = 1.0 - prob_normal
    
    # 2. Get Current Memory State
    state_snapshot = memory_store.get_state(key)
    
    # 3. Quantum Risk Assessment
    # R(x) = α P_attack + β H(x) + γ M(x)
    quantum_risk_score, entropy = calculate_quantum_risk(
        prob_normal=prob_normal,
        prob_attack=prob_attack,
        memory_state=state_snapshot
    )
    
    # 4. Update Stateful Memory & Get Escalated Risk
    # This applies Accumulation M(t+1) and Escalation R'(t)
    memory_result = memory_store.update_state(key, quantum_risk_score)
    
    return {
        "src_ip": key,
        "attack_type": attack_type,
        "classical_confidence": confidence,
        "prob_normal": prob_normal,
        "prob_attack": prob_attack,
        "entropy": entropy,
        "quantum_risk": quantum_risk_score,
        "escalated_risk": memory_result["escalated_risk"],
        "recurrence": memory_result["recurrence"],
        "memory_saturation": memory_result["memory_value"],
        "alert": memory_result["alert"]
    }
