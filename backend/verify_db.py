from app.database import SessionLocal
from app.models import NetworkEvent

db = SessionLocal()
try:
    print("------- LAST 5 EVENTS -------")
    rows = db.query(NetworkEvent).order_by(NetworkEvent.timestamp.desc()).limit(5).all()
    if not rows:
        print("❌ No events found in DB!")
    for r in rows:
        print(f"[{r.timestamp}] IP:{r.src_ip} Rate:{r.rate} Type:{r.attack_type} Risk:{r.threat_distance}")
finally:
    db.close()
