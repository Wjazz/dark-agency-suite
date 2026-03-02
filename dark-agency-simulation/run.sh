#!/bin/bash
# Dark Agency Simulation - Build and Run Script
# Usage: ./run.sh [options]

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  DARK AGENCY IN INSTITUTIONAL VOIDS - Build Script"
echo "═══════════════════════════════════════════════════════════════"

# Check for g++
if ! command -v g++ &> /dev/null; then
    echo "Error: g++ not found. Install with:"
    echo "  Fedora: sudo dnf install gcc-c++"
    echo "  Ubuntu: sudo apt install g++"
    exit 1
fi

# Create directories
mkdir -p bin output

# Compile
echo ""
echo "Compilando..."
g++ -std=c++17 -Wall -Wextra -O2 src/main.cpp -o bin/dark-agency-sim

if [ $? -eq 0 ]; then
    echo "✓ Compilación exitosa!"
    echo ""
    echo "Ejecutando simulación..."
    echo ""
    ./bin/dark-agency-sim "$@"
else
    echo "✗ Error de compilación"
    exit 1
fi
