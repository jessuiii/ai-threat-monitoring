# AI-Powered Threat Monitoring & Security Analytics Platform (UNSW-NB15 MVP)

## Overview
This project is an MVP for a modular, explainable, and confidence-aware cyber threat monitoring platform using the UNSW-NB15 dataset. It features:
- FastAPI backend (Python)
- Scikit-learn ML engine (Random Forest, Logistic Regression)
- PostgreSQL database
- React + Vite + Tailwind CSS frontend
- JWT-based authentication and RBAC
- Dockerized local deployment

## Structure
- backend/: FastAPI app, ML, API, auth
- frontend/: React dashboard
- db/: Database schema and init scripts

## Quick Start
1. Install Docker
2. Run `docker-compose up --build`
3. Access the dashboard at http://localhost:3000

## Features
- Log ingestion (API & batch)
- Log simulation (synthetic data)
- Threat detection & explainability
- What-If simulation
- Secure authentication
- Real-time dashboard

---

For details, see the MVP prompt and architecture in the project documentation.