from datetime import datetime
from sqlalchemy.orm import Session
from app.models import NetworkEvent
from app.services.ml_engine import predict_event

def handle_event(event, db: Session):
    try:
        payload = event.dict()

        result = predict_event(payload, key=payload["src_ip"])

        record = NetworkEvent(
            timestamp=datetime.fromtimestamp(payload["timestamp"]),
            src_ip=payload["src_ip"],
            rate=payload["rate"],
            spkts=payload["spkts"],
            sbytes=payload["sbytes"],
            ct_src_dport_ltm=payload["ct_src_dport_ltm"],
            ct_srv_src=payload["ct_srv_src"],
            attack_type=result["attack_type"],
            confidence=result["confidence"],
            threat_distance=result["threat_distance"],
        )

        db.add(record)
        db.commit()

        return result

    except Exception as e:
        db.rollback()
        print("❌ PIPELINE ERROR:", e)
        raise
