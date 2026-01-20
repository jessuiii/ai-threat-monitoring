import time
from attack_scenarios import generate_packet

def packet_stream():
    while True:
        yield generate_packet()
        time.sleep(0.05)
