import time
import random
from attack_scenarios import generate_packet, ATTACK_TYPES

def packet_stream():
    while True:
        attack_type = random.choices(
            ATTACK_TYPES,
            weights=[0.55, 0.12, 0.08, 0.08, 0.07, 0.06, 0.04]
        )[0]

        yield generate_packet(attack_type)
        time.sleep(0.05)
