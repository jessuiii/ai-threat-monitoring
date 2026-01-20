def classify(event):
    if event["rate"] > 100 and event["burst_rate"] > 50:
        return "dos"

    if event["ct_src_dport_ltm"] > 20:
        return "port_scan"

    if event["rate"] > 20 and event["ct_src_dport_ltm"] < 3:
        return "brute_force"

    return "normal"
