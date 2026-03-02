import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_white

# --- LABORATORIO AVANZADO: HETEROCEDASTICIDAD Y WLS ---

# 1. GENERACIÓN DE DATOS
np.random.seed(42)
N = 200
X = np.random.uniform(1, 10, N)
# Heterocedasticidad fuerte: Varianza crece con X
u = np.random.normal(0, X**2 * 0.5, N) 
Y = 10 + 2*X + u

# 2. OLS (MCO) - EL MODELO INEFICIENTE
X_const = sm.add_constant(X)
ols_model = sm.OLS(Y, X_const).fit()

print(">>> RESULTADOS OLS (INEFICIENTE) <<<")
print(f"Coeficiente X: {ols_model.params[1]:.4f}")
print(f"Std Error (Falso): {ols_model.bse[1]:.4f}")
# Usamos HC3 que es el estándar moderno
print(f"Std Error (HC3 - Robusto): {ols_model.get_robustcov_results('HC3').bse[1]:.4f}")

# 3. ESTRATEGIA FGLS (Feasible Generalized Least Squares)
residuos = ols_model.resid

# Modelamos la varianza: log(e^2) = alpha + gamma * log(X)
log_res2 = np.log(residuos**2)
log_X = np.log(X)
X_var_model = sm.add_constant(log_X)

var_model = sm.OLS(log_res2, X_var_model).fit()

# Predicción de la varianza para obtener los pesos
fitted_var_log = var_model.fittedvalues
weights = 1.0 / np.exp(fitted_var_log) 

# 4. WLS (Mínimos Cuadrados Ponderados) - EL MODELO EFICIENTE
wls_model = sm.WLS(Y, X_const, weights=weights).fit()

print("\n>>> RESULTADOS WLS (EFICIENTE - BLUE RECUPERADO) <<<")
print(f"Coeficiente X: {wls_model.params[1]:.4f}")
print(f"Std Error WLS: {wls_model.bse[1]:.4f}")

# COMPARACIÓN TÁCTICA
diff_se = ols_model.get_robustcov_results('HC3').bse[1] - wls_model.bse[1]
print("\n--- INFORME DE INTELIGENCIA ---")
print(f"Mejora de Precisión (Ganancia WLS vs HC3): {diff_se:.5f}")
print("Conclusión: WLS reduce la incertidumbre al 'castigar' la información ruidosa.")
