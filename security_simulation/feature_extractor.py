# security_simulation/feature_extractor.py
from collections import defaultdict, deque
import time

packet_count = defaultdict(int)
byte_count = defaultdict(int)
port_set = defaultdict(set)
timestamps = defaultdict(lambda: deque(maxlen=20))

def extract(packet):
    if not hasattr(packet, "ip"):
        return None

    src = packet.ip.src
    now = time.time()

    packet_count[src] += 1
    byte_count[src] += int(packet.length)
    timestamps[src].append(now)

    # Rate
    elapsed = now - timestamps[src][0] if len(timestamps[src]) > 1 else 1
    rate = packet_count[src] / elapsed

    # 🔥 Burst rate
    burst_rate = (
        len(timestamps[src]) /
        max(timestamps[src][-1] - timestamps[src][0], 0.001)
    )

    if hasattr(packet, "tcp"):
        port_set[src].add(packet.tcp.dstport)

    return {
        "timestamp": float(now),
        "src_ip": src,
        "rate": float(rate),
        "burst_rate": float(burst_rate),
        "spkts": int(packet_count[src]),
        "sbytes": int(byte_count[src]),
        "ct_src_dport_ltm": int(len(port_set[src])),
        "ct_srv_src": int(packet_count[src]),
    }
