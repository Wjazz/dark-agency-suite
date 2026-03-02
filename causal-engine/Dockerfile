FROM python:3.11-slim

WORKDIR /app

# INSTALACIÓN CRÍTICA: Librerías de sistema para Matemáticas Avanzadas
# libgomp1: Previene que Scikit-learn/Numpy colapsen (Segmentation Fault)
# libopenblas-dev: Acelera operaciones matriciales
# g++: Compilador C++ necesario para pybind11/fast_math
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    libopenblas-dev \
    liblapack-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Aumentamos el timeout por si la compilación de statsmodels es lenta
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt
# pybind11 para el bridge C++ → Python
RUN pip install --no-cache-dir pybind11>=2.11.0

COPY . .

# Compilar el módulo C++ de alto rendimiento (fast_math.so)
# El .so queda en /app/ para que FastAPI pueda importarlo con `import fast_math`
RUN python setup.py build_ext --inplace

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
