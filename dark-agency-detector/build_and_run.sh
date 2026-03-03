#!/bin/bash
# Build and Run DarkAgencyDetector
# Run this script from WSL terminal

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "  DARK AGENCY DETECTOR - Build & Run"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# Check g++
if ! command -v g++ &> /dev/null; then
    echo "❌ Error: g++ no está instalado."
    echo ""
    echo "   Para Fedora: sudo dnf install gcc-c++"
    echo "   Para Ubuntu: sudo apt install g++"
    exit 1
fi

# Create directories
mkdir -p bin frames output

# Compile
echo "📦 Compilando..."
g++ -std=c++17 -Wall -Wextra -O2 src/main.cpp -o bin/dark-agency-detector

if [ $? -eq 0 ]; then
    echo "✅ Compilación exitosa!"
    echo ""
    
    # Run with --fast to generate frames quickly
    echo "🚀 Ejecutando simulación (modo rápido para generar frames)..."
    echo ""
    ./bin/dark-agency-detector --fast
    
    # Generate GIF
    echo ""
    echo "🎬 Generando GIF..."
    
    if command -v python3 &> /dev/null; then
        if python3 -c "import PIL" 2>/dev/null; then
            python3 scripts/make_gif.py
        else
            echo "⚠️  Pillow no está instalado. Instalar con:"
            echo "   pip install Pillow"
            echo ""
            echo "   Luego ejecuta: python3 scripts/make_gif.py"
        fi
    else
        echo "⚠️  Python3 no encontrado"
    fi
else
    echo "❌ Error de compilación"
    exit 1
fi
