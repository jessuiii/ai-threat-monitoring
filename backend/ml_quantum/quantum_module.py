# quantum_module.py
import numpy as np

def calculate_entropy(probs):
    """
    H(x) = - Σ P(c|x) log P(c|x)
    """
    # Avoid log(0)
    probs = np.clip(probs, 1e-10, 1.0)
    entropy = -np.sum(probs * np.log(probs))
    return entropy

def calculate_quantum_risk(prob_normal, prob_attack, memory_state):
    """
    R(x) = α * P_attack(x) + β * H(x) + γ * M(x)
    
    Args:
        prob_normal: Probability of 'Normal' class
        prob_attack: Probability of Attack (or max attack class prob)
        memory_state: Dictionary containing 'normalized_recurrence' (M(x))
    
    Returns:
        risk_score: Float between 0 and 1
        entropy: The calculated prediction entropy
    """
    # Hyperparameters from research slides/plan
    ALPHA = 0.6  # Weight for Classical Attack Probability
    BETA  = 0.2  # Weight for Prediction Entropy (Uncertainty)
    GAMMA = 0.2  # Weight for Historical Recurrence (Memory)

    # 1. Classical Attack Probability (P_attack)
    # If the model thinks it's an attack, risk goes up.
    p_attack = prob_attack 

    # 2. Prediction Entropy (H(x))
    # We estimate entropy based on the binary split (Normal vs Attack) roughly, 
    # or we could take the full probability vector if available.
    # Here assuming we have p_normal and p_attack roughly summing to 1.
    probs = np.array([prob_normal, prob_attack])
    # Normalize just in case they don't sum to 1
    probs = probs / np.sum(probs)
    entropy = calculate_entropy(probs)
    
    # Normalize entropy to 0-1 range (max entropy for binary is ln(2) ≈ 0.693)
    normalized_entropy = min(entropy / 0.693, 1.0)

    # 3. Memory Recurrence (M(x))
    # Retrieved from stateful memory
    recurrence = memory_state.get("normalized_recurrence", 0.0)

    # 4. Quantum-Inspired Risk Function
    # R(x) = α P_attack + β H(x) + γ M(x)
    risk_score = (ALPHA * p_attack) + (BETA * normalized_entropy) + (GAMMA * recurrence)

    # Clip to ensure valid range 0-1
    risk_score = np.clip(risk_score, 0.0, 1.0)

    return risk_score, entropy
