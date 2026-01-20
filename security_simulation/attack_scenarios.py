import random
from types import SimpleNamespace

# Pool of active IPs (rotates naturally)
ACTIVE_IPS = []

def get_ip():
    # 80% reuse existing IPs
    if ACTIVE_IPS and random.random() < 0.8:
        return random.choice(ACTIVE_IPS)

    ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    ACTIVE_IPS.append(ip)

    # prevent infinite growth
    if len(ACTIVE_IPS) > 50:
        ACTIVE_IPS.pop(0)

    return ip


def generate_packet():
    ip = get_ip()
    dst_port = random.randint(1, 65535)
    size = random.randint(60, 1500)

    return SimpleNamespace(
        ip=SimpleNamespace(src=ip),
        tcp=SimpleNamespace(dstport=dst_port),
        length=size
    )
