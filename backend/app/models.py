from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, TIMESTAMP

Base = declarative_base()

class NetworkEvent(Base):
    __tablename__ = "network_events"

    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    src_ip = Column(String)
    rate = Column(Float)
    spkts = Column(Integer)
    sbytes = Column(Integer)
    ct_src_dport_ltm = Column(Integer)
    ct_srv_src = Column(Integer)

    attack_type = Column(String)
    confidence = Column(Float)
    threat_distance = Column(Float)

class ThreatState(Base):
    __tablename__ = "threat_states"

    src_ip = Column(String, primary_key=True)
    recurrence = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)
    last_seen = Column(TIMESTAMP)
