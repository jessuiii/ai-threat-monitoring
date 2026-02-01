# security_simulation/event_emitter.py
import time
import requests
from traffic_capture import packet_stream
from feature_extractor import extract

BACKEND_URL = "http://localhost:8000/events/"

def run():
    print("🚦 Traffic simulation started (PURE ML MODE)")

    session = requests.Session()

    for packet in packet_stream():
        features = extract(packet)
        if features is None:
            continue

        event = {
            "timestamp": time.time(),
            "src_ip": packet.ip.src,
            # Unpack all calculated features (dur, sload, smean, etc.)
            **features
        }

        try:
            # 🔥 SHORT timeout + no blocking retries
            session.post(
                BACKEND_URL,
                json=event,
                timeout=1.0
            )
        except requests.exceptions.RequestException:
            pass  # DROP packet silently (realistic)

        # 🔥 REMOVE HARD LIMIT to allow full speed but prevent lockup
        time.sleep(0.002)

if __name__ == "__main__":
    run()
