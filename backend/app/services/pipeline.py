from datetime import datetime
from app.database import SessionLocal
from app.models import NetworkEvent
from app.services.ml_engine import predict_event

def handle_event(event: dict):
    db = SessionLocal()
    try:
        ml = predict_event(event, key=event["src_ip"])

        record = NetworkEvent(
            timestamp=datetime.fromtimestamp(event["timestamp"]),
            src_ip=event["src_ip"],
            rate=event["rate"],
            spkts=event["spkts"],
            sbytes=event["sbytes"],
            ct_src_dport_ltm=event["ct_src_dport_ltm"],
            ct_srv_src=event["ct_srv_src"],
            prediction=ml["label"],
            confidence=ml["confidence"],
            threat_distance=ml["threat_distance"],
        )

        db.add(record)
        db.commit()
        return ml

    except Exception as e:
        db.rollback()
        return {
            "label": "ERROR",
            "confidence": 0.0,
            "threat_distance": 1.0,
            "error": str(e)
        }
    finally:
        db.close()
