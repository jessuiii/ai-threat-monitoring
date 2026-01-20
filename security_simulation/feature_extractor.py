from collections import defaultdict
import time

packet_count = defaultdict(int)
byte_count = defaultdict(int)
port_set = defaultdict(set)
last_seen = defaultdict(float)

def extract(packet):
    if not hasattr(packet, "ip"):
        return None

    src = packet.ip.src
    now = time.time()

    packet_count[src] += 1
    byte_count[src] += int(packet.length)

    elapsed = now - last_seen.get(src, now)
    rate = packet_count[src] / elapsed if elapsed > 0 else packet_count[src]
    last_seen[src] = now

    if hasattr(packet, "tcp"):
        port_set[src].add(packet.tcp.dstport)

    return {
        "timestamp": now,
        "src_ip": src,
        "rate": rate,
        "spkts": packet_count[src],
        "sbytes": byte_count[src],
        "ct_src_dport_ltm": len(port_set[src]),
        "ct_srv_src": packet_count[src]
    }
