#!/bin/bash
# AWS EC2 One-Click Deployment Script for PBEIP
set -e

echo "=== PB Equity Intelligence Platform (PBEIP) AWS Deployment ==="

# 1. System Updates & Dependencies
echo "[1/5] Updating system packages..."
sudo apt update -y
sudo apt install -y python3-pip python3-venv git tmux

# 2. Virtual Environment Setup
echo "[2/5] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python Dependencies
echo "[3/5] Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize Database & Run Initial Seed Pipeline
echo "[4/5] Initializing Database & Live Universe Pipeline..."
python3 scripts/init_db.py
python3 scripts/seed_companies.py
python3 modules/scoring/pb_score_aggregator.py
python3 modules/ranking/ranking_engine.py
python3 modules/ranking/portfolio_engine.py

# 5. Launch Streamlit Application in Background (nohup)
echo "[5/5] Launching PBEIP Terminal Server on Port 8501..."
nohup venv/bin/streamlit run modules/dashboard/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &

echo "=== Deployment Complete! ==="
echo "Access your platform at: http://$(curl -s ifconfig.me):8501"
