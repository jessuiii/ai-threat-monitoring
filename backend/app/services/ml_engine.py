import pandas as pd
try:
    from backend.ml_quantum.hybrid_ids import hybrid_decision
except ImportError:
    from ml_quantum.hybrid_ids import hybrid_decision

def predict_event(event: dict, key: str):
    # Convert single event dict to DataFrame (expected by hybrid_decision)
    # We pass index=[0] because it's a scalar row
    df = pd.DataFrame([event])
    
    # Call the Q-IDS Hybrid Engine
    result = hybrid_decision(df, key=key)
    
    # Map the detailed Q-IDS result to the fields expected by the pipeline/database
    return {
        "attack_type": result["attack_type"],
        # Use classical confidence or quantum-adjusted? Usually report specific confidence
        "confidence": result["classical_confidence"], 
        # Map 'escalated_risk' (which includes memory & quantum factors) to 'threat_distance'
        "threat_distance": result["escalated_risk"],
        
        # Extra metadata (optional, ensuring pipeline assumes only 3 fields or ignores extras)
        "quantum_risk": result["quantum_risk"],
        "entropy": result["entropy"]
    }
