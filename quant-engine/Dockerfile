FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (necesario para algunas librerías numéricas)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Ejecutar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
