import pennylane as qml
import numpy as np

# 2‑qubit quantum simulator
dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev)
def quantum_circuit(features):
    """
    Quantum circuit for risk estimation.
    features: array of 2 normalized values
    """
    qml.RY(features[0], wires=0)
    qml.RY(features[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))


def quantum_risk_score(x):
    """
    Returns a quantum‑simulated risk score in [0, 1]
    """
    x = np.array(x, dtype=float)

    # Normalize features
    x = (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-6)

    q_score = quantum_circuit(x)

    # Map from [-1, 1] → [0, 1]
    q_score = (q_score + 1) / 2

    return float(q_score)
