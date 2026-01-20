import time
import random
from attack_scenarios import generate_packet, ATTACK_TYPES

def packet_stream():
    while True:
        attack_type = random.choices(
            ATTACK_TYPES,
            weights=[0.65, 0.15, 0.10, 0.10]
        )[0]

        yield generate_packet(attack_type)
        time.sleep(0.05)
