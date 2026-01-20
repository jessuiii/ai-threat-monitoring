from datetime import datetime
from app.database import SessionLocal
from app.models import ThreatState

def get_or_create_state(src_ip: str):
    db = SessionLocal()
    try:
        state = db.query(ThreatState).filter_by(src_ip=src_ip).first()
        if not state:
            state = ThreatState(
                src_ip=src_ip,
                recurrence=0,
                risk_score=0.0,
                last_seen=datetime.utcnow()
            )
            db.add(state)
            db.commit()
            db.refresh(state)
        return state
    finally:
        db.close()

def update_state(src_ip: str, final_risk: float):
    db = SessionLocal()
    try:
        state = db.query(ThreatState).filter_by(src_ip=src_ip).first()
        state.recurrence += 1
        state.risk_score = max(state.risk_score, final_risk)
        state.last_seen = datetime.utcnow()
        db.commit()
        return state
    finally:
        db.close()
