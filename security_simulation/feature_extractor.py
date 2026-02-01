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

    # Calculate derived stats
    spkts = len(packets)
    sbytes = sum(p["size"] for p in packets)
    rate = spkts / duration
    
    # Missing features estimation (Simulated)
    # Heuristic: Web traffic (80, 443) usually has small request -> large response (High dbytes)
    # Attacks (Scanning) usually has no response or small response (Low dbytes)
    
    common_web_ports = {80, 443, 8080}
    is_web = any(p["dst_port"] in common_web_ports for p in packets)
    
    if is_web:
        dpkts = spkts * 1.5  # ACK + Data
        dbytes = sbytes * 8.0 # Download > Upload
    else:
        # Scanning / P2P / Other
        dpkts = spkts * 0.5 
        dbytes = sbytes * 0.2
        
    smean = sbytes / spkts
    dmean = dbytes / dpkts if dpkts > 0 else 0
    
    # Deduce Service Feature
    # Map common ports to service names (UNSW-NB15 style)
    # Most traffic usually has a specific service
    dst_ports = {p["dst_port"] for p in packets}
    main_port = list(dst_ports)[0] if dst_ports else 0
    
    service = "-"
    if main_port in [80, 443, 8080]: service = "http"
    elif main_port == 21: service = "ftp"
    elif main_port == 22: service = "ssh"
    elif main_port == 23: service = "telnet" # Analysis/Backdoor often
    elif main_port == 25: service = "smtp"
    elif main_port == 53: service = "dns"
    elif main_port in [110, 995]: service = "pop3"
    elif main_port in [143, 993]: service = "imap"
    
    # Use simulated metadata if available
    sim_ttl = getattr(packet, "ttl", 62)
    sim_proto = getattr(packet, "proto", "tcp")

    # Count features adjustment
    if service == "http" and is_web:
        # Normal traffic usually has low concurrent connections to same service
        ct_srv_src = 1
        ct_dst_ltm = 1
        ct_src_dport_ltm = 1
        ct_dst_sport_ltm = 1
        ct_dst_src_ltm = 1
        dbytes = sbytes * 2.0 # Moderate response (not huge download)
        sim_ttl = 31 # Common 'Normal' value
    else:
        # Attacks: Calculate actual distribution
        
        # 1. Unique ports targeted by this source
        unique_ports = {p["dst_port"] for p in packets}
        num_unique_ports = len(unique_ports)
        
        # 2. ct_src_dport_ltm: Count of connections to same dest port
        ct_src_dport_ltm = num_unique_ports # Heuristic: if scanning, this is high? No, this is "count of connections of src IP to dst port".
        # actually, if I am scanning 10 different ports, ct_src_dport_ltm for *each* flow is 1.
        # But ct_dst_ltm (same dest ip) is 10.
        
        # Let's simplify:
        ct_srv_src = len(packets)     # Services (port) accessed by source
        ct_dst_ltm = len(packets)     # Same dest IP (assuming single target)
        
        if num_unique_ports > 3:
            # SCANNNING / PROBING (Analysis, Reconnaissance)
            # Many different ports -> Low count per port
            ct_dst_sport_ltm = 1
            ct_src_dport_ltm = 1
        else:
            # DoS / FLOODING (DoS, Exploits, Fuzzers)
            # Same port repeatedly
            ct_dst_sport_ltm = len(packets)
            ct_src_dport_ltm = len(packets)
            
        ct_dst_src_ltm = len(packets)

    return {
        "dur": duration,
        "proto": sim_proto,
        "service": service,
        "state": "FIN",
        "spkts": spkts,
        "dpkts": int(dpkts),
        "sbytes": sbytes,
        "dbytes": int(dbytes),
        "rate": rate,
        "sttl": sim_ttl,
        "dttl": 252 if sim_ttl < 100 else 60,
        "sload": (sbytes * 8) / duration,
        "dload": (dbytes * 8) / duration,
        "sloss": 0,
        "dloss": 0,
        "sinpkt": duration / spkts if spkts > 0 else 0,
        "dinpkt": duration / dpkts if dpkts > 0 else 0,
        "sjit": 0,
        "djit": 0,
        "swin": 255,
        "stcpb": 1000,
        "dtcpb": 2000,
        "dwin": 255,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
        "smean": smean,
        "dmean": dmean,
        "trans_depth": 0,
        "response_body_len": 0,
        "ct_srv_src": ct_srv_src,
        "ct_state_ttl": 0,
        "ct_dst_ltm": ct_dst_ltm,
        "ct_src_dport_ltm": ct_src_dport_ltm,
        "ct_dst_sport_ltm": ct_dst_sport_ltm,
        "ct_dst_src_ltm": ct_dst_src_ltm,
        "is_ftp_login": 0,
        "ct_ftp_cmd": 0,
        "ct_flw_http_mthd": 0,
        "ct_src_ltm": len(packet_buffer), 
        "ct_srv_dst": 1,
        "is_sm_ips_ports": 0,
        "burst_rate": rate
    }
