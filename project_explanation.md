# AI Threat Monitoring System: Theoretical & Practical Explanation

## 1. Executive Summary
This project is a **Hybrid Intelligent Intrusion Detection System (IDS)** that moves beyond traditional signature-based or stateless machine learning approaches. It introduces a **stateful, adaptive risk engine** that combines:
1.  **Classical Machine Learning (Random Forest)** for baseline pattern recognition.
2.  **Quantum-Inspired Uncertainty (Entropy)** to detect ambiguous behavior.
3.  **Adaptive Memory (Recurrence)** to track and escalate persistent threats over time.

**Key Innovation**: Unlike standard IDS that forgets an IP immediately after a packet is processed, this system "remembers". A subtle probe, if repeated, accumulates "memory", eventually triggering a high-priority alert where a single event would not.

---

## 2. Theoretical Framework

The system operates on a composite risk model defined by the equation:

$$ R_{final}(t) = \underbrace{\alpha \cdot P_{attack}(t)}_{\text{Classical}} + \underbrace{\beta \cdot H(t)}_{\text{Uncertainty}} + \underbrace{\gamma \cdot M(t)}_{\text{Memory}} $$

### 2.1 Classical Machine Learning ($P_{attack}$)
- **Algorithm**: Random Forest Classifier.
- **Input**: Behavioral feature vectors (not payload).
  - `rate`: Packets per second.
  - `sbytes`, `spkts`: Volume metrics.
  - `ct_src_dport_ltm`: Destination port diversity.
- **Output**: Probability distribution over classes (Normal, Generic, Exploit, Fuzzers, DoS, etc.).
- **Role**: Provides the baseline confidence ($P_{attack}$) that a traffic flow matches known attack signatures.

### 2.2 Quantum-Inspired Uncertainty ($H$)
- **Concept**: Derived from Information Theory (Shannon Entropy), inspired by Quantum Superposition principles where a state exists in multiple possibilities.
- **Math**:
  $$ H(x) = - \sum p_i \log p_i $$
- **Role**: If the ML model is "confused" (e.g., 50% Normal, 50% Attack), Entropy is maximized. The system treats *uncertainty* as a risk factor itself. This captures novel or obfuscated attacks that sit on the decision boundary.

### 2.3 Adaptive Threat Memory ($M$)
- **Concept**: Stateful tracking of source IPs.
- **Dynamics**:
  1.  **Accumulation**: Every risky event increases the memory state $M$.
      $$ M(t+1) = M(t) + \delta \cdot R(t) $$
  2.  **Escalation**: The reported risk is boosted by the current memory level.
      $$ Risk_{escalated} = Risk_{current} + \lambda \cdot M $$
- **Result**: "Low and Slow" attacks (e.g., sending 1 packet every hour) will eventually saturate the memory $M$, causing the risk score to breach the alert threshold even if individual packets look harmless.

---

## 3. System Architecture (Practical Implementation)

The system is a Microservices-style architecture composed of three main layers:

### Layer 1: Simulation & Data Ingestion
- **Component**: `security_simulation`
- **Function**: Generates synthetic network traffic to mimic real-world scenarios.
- **Traffic Types**:
  - **Benign**: Random interactions, low volume.
  - **Attack**: Bursty logic, specific port targeting (22, 80, 445), high volume.
- **Tech**: Python, `requests` library.

### Layer 2: Hybrid Analysis Engine (Backend)
- **Component**: `backend` (FastAPI + Custom ML Modules)
- **Pipeline**:
  1.  **Event Received**: JSON payload with traffic stats.
  2.  **Classical Inference**: `ml_quantum/classical_inference.py` loads a pre-trained `.pkl` model to predict class.
  3.  **Quantum/Memory Logic**: `ml_quantum/hybrid_ids.py` manages the state.
      - **In-Memory Store**: Uses a Python `defaultdict` to store IP states in RAM for ultra-fast access.
  4.  **Persistence**: Events are logged to a SQLite/PostgreSQL database via `SQLAlchemy`.
- **API Endpoints**:
  - `POST /events/predict`: Main inference pipeline.
  - `GET /events`: Fetch history for UI.

### Layer 3: Visualization (Frontend)
- **Component**: `frontend` (React.js)
- **Function**: Real-time dashboard for SOC (Security Operations Center) analysts.
- **Features**:
  - **Polling**: Fetches `/events` every 2 seconds.
  - **Visuals**: Displays "Threat Distance" (Escalated Risk) vs "Confidence".
  - **Alerts**: Highlights IPs with $Risk > 0.8$.

---

## 4. Key Differentiators for Faculty

When presenting, emphasize these points to show depth:

1.  **Beyond Static Thresholds**: Show how a standard firewall blocks on "Port 80 > 100 requests/sec". This system blocks on "Port 80 behavior *changed* over time AND matches a generic DoS pattern".
2.  **The "Quantum" Term**: Clarify that this is **Quantum-Inspired** (mathematical modeling), not running on a Quantum Computer (QPU). It uses the math of wave functions/entropy to model uncertainty.
3.  **State Management**: Discuss the trade-off. The current implementation uses **In-Memory** state for speed (O(1) lookup), which is faster than checking a database for every packet, but means state is lost on restart (a classic distributed system trade-off).

## 5. Critical Analysis (Strengths & Limitations)

| Feature | Strength | Limitation |
| :--- | :--- | :--- |
| **Detection** | Catches "Low & Slow" attacks via Memory. | Dependent on Feature Quality (garbage in, garbage out). |
| **Performance** | High throughput (In-Memory state). | Memory usage grows with unique IP count (DoS risk). |
| **Adaptability** | Entropy catches unknown variants. | Requires tuning of $\alpha, \beta, \gamma$ weights. |
