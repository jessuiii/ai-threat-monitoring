import random
from types import SimpleNamespace

def generate_packet(attack=False):
    ip = f"192.168.1.{random.randint(2,10) if attack else random.randint(11,254)}"
    dst_port = random.choice([22, 23, 445, 3389]) if attack else random.randint(1024, 65535)
    size = random.randint(1000, 1500) if attack else random.randint(60, 400)

    return SimpleNamespace(
        ip=SimpleNamespace(src=ip),
        tcp=SimpleNamespace(dstport=dst_port),
        length=size
    )
