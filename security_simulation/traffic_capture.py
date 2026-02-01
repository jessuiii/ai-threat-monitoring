# security_simulation/traffic_capture.py
import time
from attack_scenarios import generate_packet, DOS_IP

def packet_stream():
    while True:
        pkt = generate_packet()
        yield pkt
        
        # 🔥 BURST MODE controlled by Scenario
        # Only sleep 0.001 if the attack type requires high rate (DoS, Exploits)
        is_burst = getattr(pkt, "burst", False)
        
        if is_burst:
            time.sleep(0.001) # 1000 pkts/sec
        else:
            time.sleep(0.05)  # 20 pkts/sec (Normal/Stealth)
