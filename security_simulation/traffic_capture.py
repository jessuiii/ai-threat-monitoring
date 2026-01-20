from attack_scenarios import generate_packet
import time
import random

def packet_stream():
    while True:
        attack = random.random() < 0.35  # 🔥 35% attack traffic
        yield generate_packet(attack=attack)
        time.sleep(0.05)
