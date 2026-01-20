import random
from types import SimpleNamespace

def generate_packet():
    return SimpleNamespace(
        ip=SimpleNamespace(src=f"192.168.1.{random.randint(2,254)}"),
        tcp=SimpleNamespace(dstport=random.randint(20,1024)),
        length=random.randint(60,1500)
    )
