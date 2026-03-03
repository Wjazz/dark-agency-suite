#!/bin/bash
set -e

echo "============================================================"
echo "[*] INICIANDO BUILD DEL ACELERADOR CSV EN C++ (Pybind11) [*]"
echo "============================================================"

# 1. Construir la imagen Docker que compilará el módulo C++
echo "[1/4] Construyendo contenedor de compilación..."
docker build -t csv_accel_builder .

# 2. Correr el contenedor para ejecutar el benchmark y extraer el .so
echo "[2/4] Ejecutando Benchmark C++ vs Pandas..."
# Montamos la carpeta actual para que el contenedor deje los resultados
docker run --rm -v $(pwd):/app csv_accel_builder bash -c "
    cd /app && \
    mkdir -p build && cd build && \
    cmake ../cpp && \
    make -j\$(nproc) && \
    echo '--- RESULTADOS DEL BENCHMARK ---' && \
    python3 ../python/bench_pandas.py
"

echo "[3/4] Compilación y Benchmark completados con éxito."
echo "[4/4] Artefactos generados en la carpeta build/."
echo "============================================================"
echo "Siguiente paso manual: Configurar script de ingesta a Postgres."
