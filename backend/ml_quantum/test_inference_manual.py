import pandas as pd
from backend.ml_quantum.hybrid_ids import hybrid_decision

# Create a dummy event
dummy_data = {
    "srcip": "192.168.1.100",
    "sport": 12345,
    "dstip": "10.0.0.1",
    "dsport": 80,
    "proto": "tcp",
    "state": "FIN",
    "dur": 1.5,
    "sbytes": 500,
    "dbytes": 1000,
    "sttl": 64,
    "dttl": 62,
    "service": "http",
    "Sload": 5000.0,
    "Dload": 10000.0,
    "Spkts": 10,
    "Dpkts": 12,
    "swin": 255,
    "dwin": 255,
    "stcpb": 1000,
    "dtcpb": 2000,
    "smeansz": 50,
    "dmeansz": 80,
    "trans_depth": 1,
    "res_bdy_len": 500,
    "Sjit": 10.0,
    "Djit": 12.0,
    "Stime": 1000000,
    "Ltime": 1000005,
    "Sintpkt": 5.0,
    "Dintpkt": 6.0,
    "tcprtt": 0.1,
    "synack": 0.05,
    "ackdat": 0.05,
    "is_sm_ips_ports": 0,
    "ct_state_ttl": 1,
    "ct_flw_http_mthd": 1,
    "is_ftp_login": 0,
    "ct_ftp_cmd": 0,
    "ct_srv_src": 2,
    "ct_srv_dst": 2,
    "ct_dst_ltm": 2,
    "ct_src_ltm": 2,
    "ct_src_dport_ltm": 1,
    "ct_dst_sport_ltm": 1,
    "ct_dst_src_ltm": 1,
}

df = pd.DataFrame([dummy_data])
print("🧪 Running Inference 1 (First time)...")
result1 = hybrid_decision(df, key="192.168.1.100")
print("Result 1:", result1)

print("\n🧪 Running Inference 2 (Same IP, should escalate memory)...")
result2 = hybrid_decision(df, key="192.168.1.100")
print("Result 2:", result2)

print("\n🧪 Running Inference 3 (Different IP, fresh memory)...")
result3 = hybrid_decision(df, key="192.168.1.101")
print("Result 3:", result3)
