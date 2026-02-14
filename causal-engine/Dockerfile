FROM python:3.11-slim

WORKDIR /app

# INSTALACIÓN CRÍTICA: Librerías de sistema para Matemáticas Avanzadas
# libgomp1: Previene que Scikit-learn/Numpy colapsen (Segmentation Fault)
# libopenblas-dev: Acelera operaciones matriciales
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    libopenblas-dev \
    liblapack-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Aumentamos el timeout por si la compilación de statsmodels es lenta
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
