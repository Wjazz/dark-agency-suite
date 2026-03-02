import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# --- LABORATORIO DE SERIES DE TIEMPO ---

np.random.seed(42)
n = 100

# 1. CAMINATA ALEATORIA (Random Walk) - NO ESTACIONARIA
# El precio de hoy es el precio de ayer + un shock.
# Esto simula una acción real (ej: Apple).
precio = np.cumsum(np.random.normal(0, 1, n)) 

# 2. RUIDO BLANCO (White Noise) - ESTACIONARIO
# Retornos diarios: sube y baja alrededor de 0.
retorno = np.diff(precio)

print(">>> ANÁLISIS DE ESTACIONARIEDAD (DICKEY-FULLER) <<<")

def test_stationarity(timeseries, name):
    # H0: Tiene Raíz Unitaria (No es estacionaria, es impredecible)
    # H1: Es Estacionaria (Es predecible, se puede modelar)
    result = adfuller(timeseries)
    p_value = result[1]
    
    print(f"\nSerie: {name}")
    print(f"P-value: {p_value:.5f}")
    if p_value < 0.05:
        print("RESULTADO: Rechazamos H0. La serie es ESTACIONARIA (¡Bien!).")
    else:
        print("RESULTADO: No rechazamos H0. La serie tiene RAÍZ UNITARIA (¡Peligro!).")
        print("ACCIÓN: Debes diferenciarla (usar retornos, no precios).")

test_stationarity(precio, "Precio de la Acción (Nivel)")
test_stationarity(retorno, "Retorno de la Acción (Diferencia)")
