# Usa una imagen oficial de Python basada en Debian/Ubuntu
FROM python:3.11-slim

# Instalar dependencias de compilación de C++ y pybind11-dev
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pybind11-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar paquetes de Python necesarios
RUN pip install --no-cache-dir pybind11 pytest pandas numpy psycopg2-binary

# El directorio de trabajo
WORKDIR /app

# El script demo.sh montará los archivos reales aquí mediante volúmenes
CMD ["bash"]
