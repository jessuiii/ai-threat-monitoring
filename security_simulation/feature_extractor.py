# security_simulation/feature_extractor.py
from collections import defaultdict, deque
import time

WINDOW_SECONDS = 6
packet_buffer = defaultdict(deque)

def extract(packet):
    if not hasattr(packet, "ip"):
        return None

    src = packet.ip.src
    now = time.time()

    packet_buffer[src].append({
        "time": now,
        "size": packet.length,
        "dst_port": packet.tcp.dstport,
    })

    while packet_buffer[src] and now - packet_buffer[src][0]["time"] > WINDOW_SECONDS:
        packet_buffer[src].popleft()

    # 🔥 LOWER threshold
    if len(packet_buffer[src]) < 6:
        return None

    packets = packet_buffer[src]
    duration = max(packets[-1]["time"] - packets[0]["time"], 0.001)

    return {
        "rate": len(packets) / duration,
        "spkts": len(packets),
        "sbytes": sum(p["size"] for p in packets),
        "burst_rate": len(packets) / duration,
        "ct_src_dport_ltm": len({p["dst_port"] for p in packets}),
        "ct_srv_src": len(packets),
    }
