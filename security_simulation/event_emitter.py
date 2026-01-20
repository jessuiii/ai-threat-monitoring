import pandas as pd
from traffic_capture import packet_stream
from feature_extractor import extract

from ml_quantum.classical_inference import classical_risk
from ml_quantum.alert_logic import classify_risk

def run():
    for packet in packet_stream():
        features = extract(packet)

        # No window ready yet
        if features is None:
            continue

        df = pd.DataFrame([features])

        risk = classical_risk(df)[0]
        alert = classify_risk([risk])[0]

        event = {
            **features,
            "risk_score": float(risk),
            "alert": alert
        }

        print(event)

if __name__ == "__main__":
    run()
