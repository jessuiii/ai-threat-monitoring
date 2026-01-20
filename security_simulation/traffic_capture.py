import pyshark
from attack_scenarios import generate_packet

MODE = "SIMULATED"  # LIVE or SIMULATED
INTERFACE = "Wi-Fi"

def packet_stream():
    if MODE == "LIVE":
        capture = pyshark.LiveCapture(interface=INTERFACE)
        for packet in capture.sniff_continuously():
            yield packet
    else:
        while True:
            yield generate_packet()
