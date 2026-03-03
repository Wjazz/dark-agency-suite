import pandas as pd
import numpy as np
from linearmodels.iv import IV2SLS
from typing import List, Dict, Any

class CausalInferenceEngine:
    """
    Motor de Inferencia Causal para la suite Dark Agency.
    Reemplaza los scripts monolíticos de STATA (ivregress 2sls).
    Diseñado para ser invocado por FastAPI mediante peticiones asíncronas.
    """

    @staticmethod
    def estimate_2sls(
        df: pd.DataFrame, 
        dependent: str, 
        exogenous: List[str], 
        endogenous: str, 
        instruments: List[str]
    ) -> Dict[str, Any]:
        """
        Ejecuta una regresión de Mínimos Cuadrados en 2 Etapas (Variables Instrumentales).
        
        Matemática subyacente:
        Etapa 1: endogenous ~ exogenous + instruments
        Etapa 2: dependent ~ exogenous + endogenous_hat
        """
        try:
            # 1. Asegurar que no hay valores nulos en el subset de análisis (Limpieza defensiva)
            cols_to_keep = [dependent] + exogenous + [endogenous] + instruments
            df_clean = df[cols_to_keep].dropna()

            # 2. Configurar las matrices del modelo
            Y = df_clean[dependent]
            # Se añade la constante explícitamente (el intercepto B0)
            X_exog = df_clean[exogenous].copy()
            X_exog.insert(0, 'const', 1.0) 
            
            X_endog = df_clean[endogenous]
            Instr = df_clean[instruments]

            # 3. Ensamblar y ajustar el modelo MC2E (2SLS) con errores robustos a heterocedasticidad
            model = IV2SLS(dependent=Y, exog=X_exog, endog=X_endog, instruments=Instr)
            results = model.fit(cov_type='robust')

            # 4. Extraer el valor real de la inferencia para la API (Evitamos imprimir en consola)
            # 4. Extraer el valor real de la inferencia para la API
            first_stage_f_stat = None
            is_strong = False
            
            try:
                if hasattr(results.first_stage, 'diagnostics'):
                    diag_df = results.first_stage.diagnostics
                    # Busca dinámicamente la columna que tenga 'f' y 'stat' en su nombre
                    f_col = [c for c in diag_df.columns if 'f' in c.lower() and 'stat' in c.lower()]
                    if f_col:
                        first_stage_f_stat = float(diag_df.loc[endogenous, f_col[0]])
                        is_strong = first_stage_f_stat > 10.0
            except Exception:
                pass # Si el diagnóstico falla por versión, el motor principal sigue vivo

            inference_payload = {
                "target_variable": dependent,
                "endogenous_variable": endogenous,
                "causal_effect_coef": float(results.params[endogenous]),
                "p_value": float(results.pvalues[endogenous]),
                "r_squared": float(results.rsquared),
                "first_stage_f_stat": first_stage_f_stat,
                "is_instrument_strong": is_strong,
                "model_diagnostics": "Robust covariance used (White/Huber)"
            } 

            return inference_payload

        except Exception as e:
            return {"error": f"Fallo en la estimación causal: {str(e)}"}

# =====================================================================
# EJEMPLO DE INVOCACIÓN (Simulando cómo lo llamará tu endpoint FastAPI)
# =====================================================================
if __name__ == "__main__":
    # Simulamos el DataFrame que llegaría desde tu dbt / PostgreSQL
    np.random.seed(42)
    mock_data = pd.DataFrame({
        'hours': np.random.randint(1000, 2500, 500),         # y: Horas trabajadas
        'hushrs': np.random.randint(1000, 2500, 500),        # x_endog: Horas del esposo
        'huseduc': np.random.randint(8, 20, 500),            # z: Instrumento (Educación del esposo)
        'lwage': np.random.normal(2.5, 0.5, 500),            # x_exog 1
        'educ': np.random.randint(8, 20, 500),               # x_exog 2
        'age': np.random.randint(25, 60, 500)                # x_exog 3
    })

    engine = CausalInferenceEngine()
    
    # Equivalente exacto a tu línea: 
    # ivregress 2sls hours lwage educ age (hushrs = huseduc)
    resultado = engine.estimate_2sls(
        df=mock_data,
        dependent='hours',
        exogenous=['lwage', 'educ', 'age'],
        endogenous='hushrs',
        instruments=['huseduc']
    )

    import json
    print(json.dumps(resultado, indent=4))
