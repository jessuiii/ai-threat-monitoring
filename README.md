🛡️ AI Threat Monitoring System
Hybrid ML + Adaptive Memory–Driven Network Intrusion Detection

Overview
This project is a real-time network threat monitoring system that combines:

Classical machine learning (Random Forest IDS)

Adaptive “quantum-inspired” risk modulation

Persistent threat memory stored in a database

Live attack simulation and visualization dashboard

Unlike traditional IDS systems that treat every packet independently, this system learns from repeated behavior over time and escalates risk for recurring suspicious sources, even if individual packets look benign.

What This System Actually Does
At a high level:

It watches live network-like traffic, extracts behavioral features per source IP, scores each event using a trained ML model, adapts risk based on historical behavior, stores memory in a database, and visualizes threats in real time.

In short:
It detects slow, bursty, and persistent attacks that signature-based or stateless ML systems miss.

High-Level Architecture
┌──────────────────────┐
│ Security Simulation  │
│ (Traffic Generator)  │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Feature Extraction   │
│ (rate, burst, ports) │
└─────────┬────────────┘
          │
          ▼
┌────────────────────────────────────┐
│ FastAPI Backend                     │
│  ├ Classical ML (Random Forest)     │
│  ├ Adaptive Quantum Risk Layer      │
│  ├ Threat Memory (Postgres)         │
│  └ Event Storage (Postgres)         │
└─────────┬──────────────────────────┘
          │
          ▼
┌──────────────────────┐
│ React Dashboard      │
│  ├ Live Events       │
│  └ Active Alerts     │
└──────────────────────┘
Core Components
1. Security Simulation
Simulates both benign and malicious traffic:

Normal traffic:

Random IPs

Low packet sizes

Random high ports

Attack traffic:

Repeated IPs

High burst rates

Suspicious ports (22, 23, 445, 3389)

Large packet sizes

This lets you validate detection without real network access.

2. Feature Extraction
For each source IP, the system computes:

Feature	Meaning
rate	Packets per second
burst_rate	Short-window packet intensity
spkts	Total packets seen
sbytes	Total bytes sent
ct_src_dport_ltm	Distinct destination ports
ct_srv_src	Connection count
These features capture behavioral patterns, not packet contents.

3. Classical ML Layer (Random Forest IDS)
Trained on labeled traffic data

Outputs a probability of malicious behavior

Handles:

Non-linear relationships

Mixed feature scales

Imbalanced attack data

This provides the baseline statistical risk.

4. Adaptive Quantum-Inspired Risk Layer
This is not a real quantum computer — it is quantum-inspired math.

It:

Modulates classical risk using a non-linear sine-based function

Becomes more sensitive as recurrence increases

Introduces uncertainty amplification for unstable behavior

Purpose:

Prevent attackers from staying below static thresholds

5. Threat Memory (Persistence Layer)
Each source IP has state stored in the database:

Field	Purpose
recurrence	How many times the IP was seen
risk_score	Highest observed risk
last_seen	Last activity timestamp
This enables:

Escalation over time

Long-term attacker tracking

Memory across restarts

This is the key differentiator from traditional IDS systems.

6. Hybrid Decision Engine
Final risk is computed as:

final_risk =
    α * classical_risk
  + (1 − α) * quantum_risk
  + escalation(recurrence)
This ensures:

First-time events don’t over-trigger

Persistent attackers get flagged even if subtle

7. FastAPI Backend
Responsibilities:

Accept events

Run hybrid inference

Store results

Maintain threat memory

Serve live data to frontend

Endpoints:

POST /events — ingest & store events

GET /events — fetch recent events

POST /events/predict — prediction only

8. React Frontend Dashboard
Live UI features:

Live traffic table

Threat confidence & distance

Active alert panel

Auto-refresh every 2 seconds

Alerts trigger when:

Risk crosses thresholds

Threat distance indicates instability

Repeated attackers escalate

Why Everything Was “Normal” Initially
Early on:

Burst behavior wasn’t present

Memory had no recurrence

ML model saw isolated benign patterns

Once:

Burst rate was added

Attack simulation increased

Memory persistence enabled

→ Risk escalated as designed

This is expected and correct behavior.

What Makes This Project Unique
✅ Stateful ML (memory-aware)
✅ Adaptive risk escalation
✅ Real-time simulation + detection
✅ Database-backed threat intelligence
✅ Live visualization
✅ Extensible to real packet capture

This is not just a demo — it’s an architecture pattern for modern AI-driven security systems.

How This Could Be Used in Practice
SOC threat triage

Network anomaly detection

Insider threat monitoring

Edge security systems

Research into adaptive IDS models

Final Summary
This system learns how attackers behave over time, not just what a single packet looks like.

It bridges:

Classical ML

Temporal reasoning

Adaptive risk modeling

Real-time observability

In practical terms:

It turns network noise into actionable intelligence.
