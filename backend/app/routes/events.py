from fastapi import APIRouter
from app.services.pipeline import handle_event
from app.database import SessionLocal
from app.models import NetworkEvent

router = APIRouter()

@router.post("/")
def ingest_event(event: dict):
    return handle_event(event)

@router.post("/predict")
def predict_only(event: dict):
    """
    Prediction without storing in DB
    """
    return handle_event(event)

@router.get("/")
def get_events(limit: int = 50):
    db = SessionLocal()
    try:
        events = (
            db.query(NetworkEvent)
            .order_by(NetworkEvent.id.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "src_ip": e.src_ip,
                "rate": e.rate,
                "spkts": e.spkts,
                "sbytes": e.sbytes,
                "prediction": e.prediction,
                "confidence": e.confidence,
                "threat_distance": e.threat_distance,
            }
            for e in events
        ]
    finally:
        db.close()
