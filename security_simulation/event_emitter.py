import requests
from traffic_capture import packet_stream
from feature_extractor import extract
from attack_classifier import classify

BACKEND_URL = "http://localhost:8000/events/"

def run():
    for packet in packet_stream():
        event = extract(packet)
        if event:
            event["predicted_attack"] = classify(event)
            requests.post(BACKEND_URL, json=event, timeout=5)
            print(event)

if __name__ == "__main__":
    run()
