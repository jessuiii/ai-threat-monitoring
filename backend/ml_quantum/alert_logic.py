def classify_risk(final_risk):
    labels = []
    for r in final_risk:
        if r >= 0.6:
            labels.append("🚨 High Risk")
        elif r >= 0.35:
            labels.append("⚠️ Suspicious")
        else:
            labels.append("✅ Normal")
    return labels
