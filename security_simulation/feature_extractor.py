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

    elapsed = now - timestamps[src][0] if len(timestamps[src]) > 1 else 1
    rate = packet_count[src] / elapsed

    burst_rate = len(timestamps[src]) / max(
        timestamps[src][-1] - timestamps[src][0], 0.001
    )

    if hasattr(packet, "tcp"):
        port_set[src].add(packet.tcp.dstport)

    return {
        "timestamp": now,
        "src_ip": src,
        "rate": rate,
        "burst_rate": burst_rate,
        "spkts": packet_count[src],
        "sbytes": byte_count[src],
        "ct_src_dport_ltm": len(port_set[src]),
        "ct_srv_src": packet_count[src],
        "true_attack": packet.attack_type
    }
