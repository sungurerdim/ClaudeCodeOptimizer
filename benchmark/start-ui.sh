#!/bin/bash
cd "$(dirname "$0")"

# Default port (8765 often blocked by Windows Hyper-V)
PORT=${1:-5000}

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║        CCO Benchmark v1.0             ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found. Please install Python 3.10+"
    exit 1
fi

# Check/install dependencies
echo "[1/2] Checking dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt -q
fi

# Start server
echo "[2/2] Starting server..."
echo ""
echo "  Dashboard: http://localhost:$PORT"
echo "  Press Ctrl+C to stop"
echo ""

python3 -m benchmark --port $PORT
