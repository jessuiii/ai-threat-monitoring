from pydantic import BaseModel
from datetime import datetime

class NetworkEventIn(BaseModel):
    timestamp: datetime
    src_ip: str
    rate: float
    spkts: int
    sbytes: int
    ct_src_dport_ltm: int
    ct_srv_src: int

class PredictionOut(BaseModel):
    label: str
    confidence: float
    threat_distance: float
