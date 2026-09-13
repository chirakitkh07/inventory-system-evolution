#!/usr/bin/env bash
# setup.sh — Clean environment setup script for Inventory Management System v2.0
# Usage: bash setup.sh

set -euo pipefail

echo "=== Inventory Management System — Setup ==="

# 1. Check Python version
python3 --version || { echo "❌ Python3 not found. Please install Python 3.10+."; exit 1; }

# 2. Create virtual environment
echo "→ Creating virtual environment..."
python3 -m venv .venv

# 3. Activate and install dependencies
echo "→ Installing dependencies..."
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 4. Copy env template if not present
if [ ! -f .env ]; then
    cp .env.example .env
    echo "→ .env created from .env.example — please review settings."
fi

# 5. Smoke test
echo "→ Running smoke tests..."
python -m pytest test_app.py tests/ -q --tb=short

echo ""
echo "✅ Setup complete. Run: python main.py"
