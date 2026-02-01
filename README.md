# 🛡️ AI Threat Monitoring System
### Hybrid ML + Adaptive Memory–Driven Network Intrusion Detection

---

## 📖 Overview

This project is a **real-time network threat monitoring system** that combines:
- **Classical Machine Learning**: Random Forest–based IDS (Intrusion Detection System).
- **Adaptive Quantum-Inspired Risk**: Non-linear risk modulation based on behavior entropy.
- **Persistent Threat Memory**: Database-backed tracking of suspicious IPs over time.
- **Live Visualization**: Real-time dashboard for monitoring network traffic and identifying advanced persistent threats.

Unlike traditional IDS that treat every packet independently, this system **learns from repeated behavior over time**, escalating risk for recurring suspicious sources even when individual packets appear benign.

---

## 🏗️ Architecture & Core Components

### 1. Security Simulation (Traffic Generator)
Simulates realistic network traffic patterns for testing without needing a real physical network tap.
- **Normal Traffic**: Web browsing, DNS queries, random high ports.
- **Attack Variations**: 
    - **DoS**: High-frequency packet bursts.
    - **Exploits**: Payload-heavy traffic targeting web ports.
    - **Reconnaissance**: Low-volume port scanning.
    - **Burst Mode**: Simulates rapid fire attacks vs. slow-and-low evasion.

### 2. Feature Extractor
Converts raw packet data into behavioral features:
- `rate`: Packets per second per IP.
- `burst_rate`: Short-window intensity.
- `ct_src_dport_ltm`: Count of distinct destination ports.
- `sbytes/spkts`: Volume metrics.

### 3. Classical ML Layer (Random Forest)
A pre-trained **Random Forest Classifier** evaluates features to predict the probability of known attack classes (DoS, Analysis, Backdoor, Fuzzers, etc.). It provides the *baseline* statistical confidence.

### 4. Quantum-Inspired Risk Engine & Threat Memory
This is the **"Adaptive Brain"** of the system.
- **Threat Memory**: A persistent database (sqlite/postgres) tracks `recurrence` (how often an IP is seen) and `history_score`.
- **Quantum-Inspired Logic**: Uses non-linear functions (sine/entropy) to modulate risk.
    - *Entropy*: Measures the instability of an attacker's behavior.
    - *Escalation*: If an IP returns repeatedly, the system amplifies the risk score, catching "low and slow" attacks that might slip past the static ML model.

### 5. Frontend Dashboard
A simplified, high-performance **React** UI that shows:
- **Live Traffic Table**: Real-time stream of packet events.
- **Threat Metrics**: Visualizes `Confidence` (ML probability) and `Threat Distance` (Escalated Risk).
- **Active Alerts**: Instant notifications for high-risk IPs.

---

## 🚀 Getting Started From Scratch

Follow these steps to set up the entire project on your local machine.

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/jessuiii/ai-threat-monitoring.git
cd ai-threat-monitoring
```

---

### 3. Backend Setup
The backend handles data ingestion, ML inference, and the database.

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment**:
    - **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
    - **Mac/Linux**: `source venv/bin/activate`
3.  **Install dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

---

### 4. Frontend Setup
The frontend is a React application built with Vite.

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install Node dependencies**:
    ```bash
    npm install
    ```

---

## 🏃‍♂️ Running the Application

You will need **three separate terminal instances** to run the full system.

### Terminal 1: Backend Server
Runs the FastAPI server at `http://127.0.0.1:8000`.

```powershell
# From project root, activate venv first
.\venv\Scripts\Activate.ps1

# CRITICAL: Navigate to backend directory to ensure imports work correctly
cd backend

# Run the server
python -m uvicorn app.main:app --reload
```

### Terminal 2: Frontend Dashboard
Runs the React UI at `http://localhost:5173`.

```powershell
# From project root
cd frontend

# Start the dev server
npm run dev
```

### Terminal 3: Security Simulation
Generates synthetic network traffic.

```powershell
# From project root, activate venv
.\venv\Scripts\Activate.ps1

# Navigate to simulation folder
cd security_simulation

# Run the event emitter
python event_emitter.py
```


---

## � Project Structure

```graphql
project2/
├── backend/                # FastAPI Application & ML Models
│   ├── app/                # API Routes & Schemas
│   ├── ml_quantum/         # Hybrid ML + Quantum Logic
│   └── requirements.txt    # Python Dependencies
├── frontend/               # React Dashboard
│   ├── src/
│   │   ├── components/     # UI Components (LiveTable, Alerts)
│   │   └── pages/          # Main Views
│   └── package.json        # Node Dependencies
├── security_simulation/    # Traffic Generators
│   ├── attack_scenarios.py # Attack Logic (DoS, Exploits, etc.)
│   └── event_emitter.py    # Main script to stream events
├── dataset/                # Dataset storage
└── outputs/                # Logs and model outputs
```

---

## �🛠️ Troubleshooting

- **ModuleNotFoundError: No module named 'app'**  
  Ensure you are in the `backend/` directory when running `uvicorn`.

- **Frontend showing "Disconnected"**  
  Verify the backend is running on port 8000.

---
*Built for Advanced Agentic Coding - Google Deepmind*
