import random
from types import SimpleNamespace

ATTACK_TYPES = [
    "normal",
    "dos",
    "reconnaissance",
    "port_scan",
    "brute_force",
    "exploits",
    "fuzzer"
]

def generate_packet(attack_type="normal"):
    if attack_type == "dos":
        ip = "192.168.1.5"
        dst_port = random.randint(80, 443)
        size = random.randint(1200, 1500)

    elif attack_type == "reconnaissance":
        ip = "192.168.1.6"
        dst_port = random.randint(1, 1024)
        size = random.randint(60, 300)

    elif attack_type == "port_scan":
        ip = "192.168.1.7"
        dst_port = random.randint(1, 65535)
        size = random.randint(60, 200)

    elif attack_type == "brute_force":
        ip = "192.168.1.8"
        dst_port = random.choice([22, 23, 3389])
        size = random.randint(200, 500)

    elif attack_type == "exploits":
        ip = "192.168.1.9"
        dst_port = random.choice([80, 443, 8080])
        size = random.randint(500, 900)

    elif attack_type == "fuzzer":
        ip = "192.168.1.10"
        dst_port = random.randint(1, 65535)
        size = random.randint(1, 1500)

    else:  # normal
        ip = f"192.168.1.{random.randint(20,254)}"
        dst_port = random.randint(1024, 65535)
        size = random.randint(60, 400)

    return SimpleNamespace(
        ip=SimpleNamespace(src=ip),
        tcp=SimpleNamespace(dstport=dst_port),
        length=size,
        attack_type=attack_type
    )
