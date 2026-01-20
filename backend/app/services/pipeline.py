# app/services/pipeline.py
from datetime import datetime
from app.database import SessionLocal
from app.models import NetworkEvent
from app.services.ml_engine import predict_event


def handle_event(event: dict):
    print("🔥 Incoming event:", event)
    db = SessionLocal()

    try:
        result = predict_event(event, key=event["src_ip"])

        record = NetworkEvent(
            timestamp=datetime.fromtimestamp(event["timestamp"]),
            src_ip=event["src_ip"],
            rate=event["rate"],
            spkts=event["spkts"],
            sbytes=event["sbytes"],
            ct_src_dport_ltm=event["ct_src_dport_ltm"],
            ct_srv_src=event["ct_srv_src"],

            # 🔥 UPDATED
            attack_type=result["attack_type"],
            confidence=result["confidence"],
            threat_distance=result["threat_distance"],
        )

        db.add(record)
        db.commit()

        return result

    except Exception as e:
        db.rollback()
        print("❌ DB ERROR:", e)
        raise e

    finally:
        db.close()
