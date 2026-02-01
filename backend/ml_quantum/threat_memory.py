# threat_memory.py
from collections import defaultdict
from datetime import datetime

class ThreatMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: {
            "risk_accumulator": 0.0,
            "recurrence": 0,
            "normalized_recurrence": 0.0,
            "last_seen": None
        })
        
        # Hyperparameters
        self.DELTA = 0.01  # Memory accumulation rate
        self.LAMBDA = 0.5  # Risk escalation factor
        self.THETA = 0.8   # Alert threshold

    def get_state(self, key):
        return self.memory[key]

    def update_state(self, key, current_risk):
        """
        Updates memory state based on current risk.
        
        M(t+1) = M(t) + delta * R(t)
        R'(t)  = R(t) + lambda * M(t)
        """
        m = self.memory[key]
        
        # 1. Update Recurrence Count
        m["recurrence"] += 1
        m["last_seen"] = datetime.utcnow()
        
        # 2. Accumulate Memory: M(t+1) = M(t) + delta * R(t)
        # We cap normalized_recurrence at 1.0 to prevent infinite growth
        m["normalized_recurrence"] = min(m["normalized_recurrence"] + (self.DELTA * current_risk), 1.0)
        
        # 3. Progressive Risk Escalation: R'(t) = R(t) + lambda * M(t)
        escalated_risk = current_risk + (self.LAMBDA * m["normalized_recurrence"])
        
        # Cap escalated risk at 1.0
        escalated_risk = min(escalated_risk, 1.0)
        
        # 4. Check Alert Condition
        alert = escalated_risk >= self.THETA
        
        return {
            "escalated_risk": escalated_risk,
            "memory_value": m["normalized_recurrence"],
            "recurrence": m["recurrence"],
            "alert": alert
        }
