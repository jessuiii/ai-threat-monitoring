from collections import defaultdict, deque
import time

WINDOW_SECONDS = 10

packet_buffer = defaultdict(deque)
session_start = {}

def extract(packet):
    if not hasattr(packet, "ip"):
        return None

    src = packet.ip.src
    now = time.time()

    if src not in session_start:
        session_start[src] = now

    # Store packet info
    packet_buffer[src].append({
        "time": now,
        "size": packet.length,
        "dst_port": packet.tcp.dstport
    })

    # Remove expired packets
    while packet_buffer[src] and now - packet_buffer[src][0]["time"] > WINDOW_SECONDS:
        packet_buffer[src].popleft()

    # Wait until window has enough data
    if len(packet_buffer[src]) < 10:
        return None

    packets = packet_buffer[src]

    times = [p["time"] for p in packets]
    sizes = [p["size"] for p in packets]
    ports = {p["dst_port"] for p in packets}

    duration = max(times) - min(times)
    duration = max(duration, 0.001)

    return {
        "spkts": len(packets),
        "sbytes": sum(sizes),
        "rate": len(packets) / duration,
        "burst_rate": len(packets) / duration,
        "ct_src_dport_ltm": len(ports),
        "session_duration": now - session_start[src],
    }
