#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "[BOT] Installing dependencies..."
pip install -r requirements.txt -q

echo "[BOT] Starting Highrise Bot..."
python main.py
