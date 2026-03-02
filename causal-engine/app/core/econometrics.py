import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression

class CausalInference:
    """
    Motor de Inferencia Causal para Evaluación de Impacto.
    Implementa Control Sintético y Variables Instrumentales.
    """

    @staticmethod
    def synthetic_control(target_series: list, control_pool: list):
        """
        Construye un 'Doppelgänger' sintético del target usando una combinación lineal
        de las unidades de control. Minimiza la diferencia en el periodo pre-intervención.
        
        Args:
            target_series: Datos históricos de la unidad tratada (ej: Ventas en Perú).
            control_pool: Lista de listas con datos de unidades de control (ej: Chile, Colombia).
        """
        X0 = np.array(control_pool).T  # Matriz de controles (Time x Units)
        y = np.array(target_series)    # Vector target (Time x 1)
        
        n_controls = X0.shape[1]
        
        # Función de pérdida: Diferencia al cuadrado entre Target y Sintético
        def loss(W):
            diff = y - X0 @ W
            return np.sum(diff**2)
        
        # Restricciones: Los pesos suman 1 y son no-negativos (Convex Hull)
        constraints = ({'type': 'eq', 'fun': lambda W: np.sum(W) - 1})
        bounds = [(0, 1) for _ in range(n_controls)]
        
        # Optimización (Encontrar los pesos W)
        W_init = np.ones(n_controls) / n_controls
        result = minimize(loss, W_init, method='SLSQP', bounds=bounds, constraints=constraints)
        
        optimal_weights = result.x
        synthetic_y = X0 @ optimal_weights
        
        return {
            "optimal_weights": list(np.round(optimal_weights, 4)),
            "synthetic_series": list(np.round(synthetic_y, 2)),
            "fit_error_rmse": round(np.sqrt(result.fun / len(y)), 4)
        }

    @staticmethod
    def instrumental_variables(y, x, z):
        """
        Realiza Mínimos Cuadrados en Dos Etapas (2SLS) para corregir endogeneidad.
        y = Variable dependiente (ej: PIB)
        x = Variable endógena (ej: Instituciones)
        z = Instrumento (ej: Mortalidad de colonos - Acemoglu)
        """
        # Etapa 1: Regresión de X sobre Z (X_hat = a + bZ)
        # Usamos statsmodels para tener estadísticas robustas
        Z_cons = sm.add_constant(z)
        first_stage = sm.OLS(x, Z_cons).fit()
        x_hat = first_stage.predict(Z_cons)
        
        # Etapa 2: Regresión de Y sobre X_hat (Y = c + d*X_hat)
        X_hat_cons = sm.add_constant(x_hat)
        second_stage = sm.OLS(y, X_hat_cons).fit()
        
        return {
            "coefficient_iv": round(second_stage.params[1], 4),
            "std_error": round(second_stage.bse[1], 4),
            "t_statistic": round(second_stage.tvalues[1], 4),
            "first_stage_f_stat": round(first_stage.fvalue, 2), # Para ver si el instrumento es fuerte
            "interpretation": "Strong Instrument" if first_stage.fvalue > 10 else "Weak Instrument (Caution)"
        }
