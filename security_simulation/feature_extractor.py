from collections import defaultdict, deque
import time

packet_count = defaultdict(int)
byte_count = defaultdict(int)
port_set = defaultdict(set)
timestamps = defaultdict(lambda: deque(maxlen=50))
session_start = {}

def extract(packet):
    if not hasattr(packet, "ip"):
        return None

    src = packet.ip.src
    now = time.time()

    packet_count[src] += 1
    byte_count[src] += packet.length
    port_set[src].add(packet.tcp.dstport)
    timestamps[src].append(now)

    if src not in session_start:
        session_start[src] = now

    elapsed = now - timestamps[src][0] if len(timestamps[src]) > 1 else 1

    return {
        # These names MUST exist in train.csv FEATURES
        "spkts": packet_count[src],
        "sbytes": byte_count[src],
        "rate": packet_count[src] / elapsed,
        "burst_rate": len(timestamps[src]) / max(
            timestamps[src][-1] - timestamps[src][0], 0.001
        ),
        "ct_src_dport_ltm": len(port_set[src]),
        "session_duration": now - session_start[src],
    }
