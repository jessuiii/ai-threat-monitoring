# hybrid_ids.py
from ml_quantum.classical_inference import classical_risk
from ml_quantum.quantum_module import adaptive_quantum_risk
from ml_quantum.threat_memory import ThreatMemory

memory_store = ThreatMemory()

def hybrid_decision(df, key, alpha=0.7):
    classical = classical_risk(df)[0]
    memory = memory_store.get(key)

    quantum = adaptive_quantum_risk(classical, memory)
    final = alpha * classical + (1 - alpha) * quantum

    memory_store.update(key, final, classical)

    return classical, quantum, final
