# quantum_module.py
import numpy as np

def adaptive_quantum_risk(classical_prob, memory):
    adaptive_factor = 1 + min(memory["recurrence"] * 0.05, 1.0)
    phase_shift = memory["confidence_drift"]

    theta = classical_prob * np.pi * adaptive_factor
    quantum_prob = np.sin(theta + phase_shift) ** 2

    return quantum_prob
