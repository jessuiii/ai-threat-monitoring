from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import NetworkEventIn, PredictionOut
from app.services.pipeline import handle_event

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PredictionOut)
def ingest_event(event: NetworkEventIn, db: Session = Depends(get_db)):
    return handle_event(event, db)

@router.get("/")
def get_events(limit: int = 50, db: Session = Depends(get_db)):
    from app.models import NetworkEvent

    rows = (
        db.query(NetworkEvent)
        .order_by(NetworkEvent.timestamp.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "src_ip": r.src_ip,
            "rate": r.rate,
            "spkts": r.spkts,
            "sbytes": r.sbytes,
            "attack_type": r.attack_type,
            "confidence": r.confidence,
            "threat_distance": r.threat_distance,
        }
        for r in rows
    ]
