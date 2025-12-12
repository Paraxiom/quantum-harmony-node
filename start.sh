#!/bin/bash
# QuantumHarmony Node Operator - One-click start

cd "$(dirname "$0")"

echo "QuantumHarmony Node Operator"
echo "============================"
echo ""

# Check for node binary
if [ ! -f "./quantumharmony-node" ]; then
    echo "Node binary not found. Downloading..."
    # TODO: Add download URL when available
    echo "Please place quantumharmony-node binary in this directory"
    echo ""
fi

# Start dashboard (includes node control)
echo "Starting dashboard at http://localhost:9955"
echo "Press Ctrl+C to stop"
echo ""

cd dashboard
python3 run.py
