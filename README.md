
# AI-Powered Threat Monitoring & Security Analytics Platform
### UNSW-NB15 — MVP

## Overview

This repository contains a **minimum viable product (MVP)** for an AI-powered cyber threat monitoring and security analytics platform built using the **UNSW-NB15 intrusion detection dataset**.

The project focuses on detecting, simulating, and analyzing network-based threats using classical machine learning models, a backend API, and a modern frontend dashboard. It is designed to be modular, explainable, and extensible for research, learning, and portfolio demonstration.

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Machine Learning:** Scikit-learn (Random Forest, Logistic Regression)
- **Frontend:** React, Vite, Tailwind CSS
- **Data:** UNSW-NB15 dataset (CSV format)
- **Simulation:** Custom Python scripts for synthetic attack and traffic generation

---

## Project Structure

```

backend/                 # FastAPI backend and ML services
│── app/
│   ├── routes/          # API routes
│   ├── services/        # ML pipelines and inference logic
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py     # Database utilities
│
│── ml_quantum/          # ML and hybrid threat detection modules
│
frontend/                # React dashboard (Vite + Tailwind)
│── src/
│   ├── components/
│   ├── pages/
│
dataset/                 # UNSW-NB15 data and metadata
security_simulation/     # Attack traffic and log simulation tools

````

---

## Features

- API-based log ingestion (batch and simulated data)
- Machine-learning-driven intrusion detection
- Modular ML training, inference, and evaluation pipelines
- Synthetic attack and network traffic simulation
- Confidence-aware predictions
- Interactive frontend dashboard for alerts and live monitoring
- Clean and scalable project architecture

---

## Local Setup (Without Docker)

### 1. Clone the repository

```bash
git clone https://github.com/jessuiii/ai-threat-monitoring.git
cd ai-threat-monitoring
````

---

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server:

```bash
uvicorn app.main:app --reload
```

Backend API will be available at:

```
http://127.0.0.1:8000
```

---

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend application will be available at:

```
http://localhost:5173
```

---

## Use Cases

* AI-assisted intrusion detection research
* Security analytics and SOC dashboard prototyping
* Machine learning experimentation on network traffic data
* Academic, learning, and portfolio cybersecurity projects

---

## MVP Scope & Future Improvements

This project currently represents an **early-stage MVP**. Planned future enhancements include:

* Advanced model explainability and visualization
* Real-time data streaming and ingestion
* Authentication and role-based access control
* Alerting and notification pipelines
* Production-ready deployment workflows

---

## Dataset

This project uses the **UNSW-NB15** dataset for training and evaluation.
The dataset is widely used in intrusion detection research and contains both normal and malicious network traffic samples.


---

This repository is intended for **educational, research, and demonstration purposes**.

```

