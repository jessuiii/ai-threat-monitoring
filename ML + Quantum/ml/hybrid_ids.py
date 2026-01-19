from classical_inference import classical_risk
from quantum_module import quantum_risk

def hybrid_decision(df, alpha=0.7):
    classical = classical_risk(df)
    quantum = quantum_risk(classical)

    # Hybrid weighted fusion
    final_risk = alpha * classical + (1 - alpha) * quantum

    return classical, quantum, final_risk
