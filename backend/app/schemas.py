from pydantic import BaseModel
from datetime import datetime

class NetworkEventIn(BaseModel):
    timestamp: float
    src_ip: str
    rate: float
    spkts: int
    sbytes: int
    ct_src_dport_ltm: int
    ct_srv_src: int
    burst_rate: float | None = 0.0

class PredictionOut(BaseModel):
    attack_type: str
    confidence: float
    threat_distance: float
