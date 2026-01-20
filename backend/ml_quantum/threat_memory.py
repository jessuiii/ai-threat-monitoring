# threat_memory.py
from collections import defaultdict
from datetime import datetime

class ThreatMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: {
            "risk_accumulator": 0.0,
            "recurrence": 0,
            "volatility": 0.0,
            "confidence_drift": 0.0,
            "last_seen": None
        })

    def get(self, key):
        return self.memory[key]

    def update(self, key, risk, confidence):
        m = self.memory[key]
        m["risk_accumulator"] += risk
        m["recurrence"] += 1
        m["confidence_drift"] = abs(m["risk_accumulator"] / m["recurrence"] - confidence)
        m["last_seen"] = datetime.utcnow()
