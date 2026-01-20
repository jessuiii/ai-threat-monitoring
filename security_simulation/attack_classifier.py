def classify(event):
    if event["rate"] > 120 and event["burst_rate"] > 60:
        return "dos"

    if event["ct_src_dport_ltm"] > 30:
        return "port_scan"

    if 10 < event["rate"] < 40 and event["ct_src_dport_ltm"] > 10:
        return "reconnaissance"

    if event["rate"] > 20 and event["ct_src_dport_ltm"] < 3:
        return "brute_force"

    if 5 < event["rate"] < 20 and event["avg_pkt_size"] > 500:
        return "exploits"

    if event["avg_pkt_size"] < 100 or event["avg_pkt_size"] > 1300:
        return "fuzzer"

    return "normal"
