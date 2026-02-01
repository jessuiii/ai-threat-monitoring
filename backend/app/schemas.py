from pydantic import BaseModel
from datetime import datetime

class NetworkEventIn(BaseModel):
    timestamp: float
    src_ip: str
    # Core legacy fields (kept for documentation), but model will accept ANY extra fields
    rate: float | None = None
    spkts: int | None = None
    sbytes: int | None = None
    ct_src_dport_ltm: int | None = None
    ct_srv_src: int | None = None
    service: str | None = None # NEW
    burst_rate: float | None = 0.0

    class Config:
        extra = "allow"

class PredictionOut(BaseModel):
    attack_type: str
    confidence: float
    threat_distance: float
