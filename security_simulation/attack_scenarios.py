import random
from types import SimpleNamespace

ATTACK_TYPES = [
    "normal", "dos", "reconnaissance", "port_scan",
    "brute_force", "exploits", "fuzzer",
    "backdoor", "shellcode", "worm"
]

def generate_packet():
    ip = f"192.168.1.{random.randint(2,254)}"
    dst_port = random.randint(1, 65535)
    size = random.randint(60, 1500)

    return SimpleNamespace(
        ip=SimpleNamespace(src=ip),
        tcp=SimpleNamespace(dstport=dst_port),
        length=size
    )
