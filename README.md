# 🛡️ AI Threat Monitoring System
### Hybrid ML + Adaptive Memory–Driven Network Intrusion Detection

---

## Overview

This project is a **real-time network threat monitoring system** that combines:

- Classical machine learning (Random Forest–based IDS)
- Adaptive *quantum-inspired* risk modulation
- Persistent threat memory stored in a database
- Live attack simulation and visualization dashboard

Unlike traditional intrusion detection systems (IDS) that treat every packet independently, this system **learns from repeated behavior over time**. It escalates risk for recurring suspicious sources even when individual packets appear benign.

---

## What This System Does

At a high level, the system:

- Observes live, network-like traffic
- Extracts behavioral features per source IP
- Scores each event using a trained ML model
- Adapts risk based on historical behavior
- Persists threat memory in a database
- Visualizes threats in real time via a dashboard

**In short:**  
It detects **slow, bursty, and persistent attacks** that signature-based or stateless ML systems often miss.


---

## Core Components

### 1. Security Simulation

Simulates both benign and malicious network traffic.

**Normal traffic**
- Random IP addresses
- Low packet sizes
- Random high ports

**Attack traffic**
- Repeated source IPs
- High burst rates
- Suspicious ports (22, 23, 445, 3389)
- Large packet sizes

This enables safe validation without real network access.

---

### 2. Feature Extraction

For each source IP, the system computes behavioral features:

| Feature | Description |
|------|-----------|
| rate | Packets per second |
| burst_rate | Short-window packet intensity |
| spkts | Total packets seen |
| sbytes | Total bytes sent |
| ct_src_dport_ltm | Distinct destination ports |
| ct_srv_src | Connection count |

These features capture **behavioral patterns**, not packet payloads.

---

### 3. Classical ML Layer (Random Forest IDS)

- Trained on labeled network traffic data
- Outputs probability of malicious behavior
- Handles non-linear relationships and class imbalance

This layer provides the **baseline statistical risk score**.

---

### 4. Adaptive Quantum-Inspired Risk Layer

This is **quantum-inspired mathematics**, not a real quantum computer.

It:
- Modulates classical risk using non-linear sine-based functions
- Increases sensitivity as recurrence grows
- Amplifies uncertainty for unstable behavior

**Purpose:**  
Prevent attackers from staying below static thresholds.

---

### 5. Threat Memory (Persistence Layer)

Each source IP has persistent state stored in the database:

| Field | Purpose |
|----|-------|
| recurrence | Number of times IP observed |
| risk_score | Highest observed risk |
| last_seen | Last activity timestamp |

This enables:
- Risk escalation over time
- Long-term attacker tracking
- Memory across system restarts

This is the **key differentiator** from traditional IDS systems.

---

### 6. Hybrid Decision Engine

Final risk is computed as:

final_risk =
α * classical_risk

(1 − α) * quantum_risk

escalation(recurrence)


This ensures:
- First-time events don’t over-trigger
- Persistent attackers are flagged even when subtle

---

### 7. FastAPI Backend

Responsibilities:
- Accept events
- Run hybrid inference
- Store results
- Maintain threat memory
- Serve live data to frontend

**Key Endpoints**
- `POST /events` — ingest and store events
- `GET /events` — fetch recent events
- `POST /events/predict` — prediction-only inference

---

### 8. React Frontend Dashboard

Live UI features:
- Live traffic table
- Threat confidence and distance metrics
- Active alert panel
- Auto-refresh every 2 seconds

Alerts trigger when:
- Risk exceeds thresholds
- Threat distance indicates instability
- Recurring attackers escalate

---

## Why Everything Looked “Normal” Initially

Early in execution:
- Burst behavior was absent
- Threat memory had no recurrence
- ML model saw isolated benign patterns

Once:
- Burst rates increased
- Attack simulation intensified
- Memory persistence activated

➡️ Risk escalation occurred **as designed**.

This behavior is expected and correct.

---

## What Makes This Project Unique

✅ Stateful ML with memory awareness  
✅ Adaptive risk escalation  
✅ Real-time simulation and detection  
✅ Database-backed threat intelligence  
✅ Live visualization  
✅ Extensible to real packet capture  

This is not just a demo — it is an **architecture pattern for modern AI-driven security systems**.

---

## Practical Use Cases

- SOC threat triage
- Network anomaly detection
- Insider threat monitoring
- Edge security systems
- Research on adaptive IDS models

---

## Final Summary

This system learns **how attackers behave over time**, not just what a single packet looks like.

It bridges:
- Classical machine learning
- Temporal reasoning
- Adaptive risk modeling
- Real-time observability

**In practical terms:**  
It turns network noise into **actionable intelligence**.

