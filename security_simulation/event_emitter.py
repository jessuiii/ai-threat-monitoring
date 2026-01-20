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
            "rate": features["rate"],
            "spkts": features["spkts"],
            "sbytes": features["sbytes"],
            "ct_src_dport_ltm": features["ct_src_dport_ltm"],
            "ct_srv_src": features["ct_srv_src"],
            "burst_rate": features["burst_rate"],
        }

        try:
            # 🔥 SHORT timeout + no blocking retries
            session.post(
                BACKEND_URL,
                json=event,
                timeout=0.3
            )
        except requests.exceptions.RequestException:
            pass  # DROP packet silently (realistic)

        # 🔥 HARD RATE LIMIT
        time.sleep(0.15)  # ~6–7 events/sec

if __name__ == "__main__":
    run()
