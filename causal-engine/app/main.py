from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from app.core.econometrics import CausalInference

app = FastAPI(
    title="Dark Agency Causal Engine",
    version="1.0.0",
    description="Motor de Inferencia Causal: Control Sintético & Variables Instrumentales"
)

class SyntheticRequest(BaseModel):
    target_pre_intervention: List[float] = Field(..., description="Datos históricos antes del evento")
    controls_pre_intervention: List[List[float]] = Field(..., description="Matriz de datos de competidores/países control")

class IVRequest(BaseModel):
    outcome_y: List[float] = Field(..., description="Variable Dependiente (ej: GDP)")
    endogenous_x: List[float] = Field(..., description="Variable Explicativa Endógena (ej: Instituciones)")
    instrument_z: List[float] = Field(..., description="Instrumento Exógeno (ej: Mortalidad Colonos)")

@app.post("/synthetic-control")
def run_synthetic_control(data: SyntheticRequest):
    result = CausalInference.synthetic_control(
        data.target_pre_intervention,
        data.controls_pre_intervention
    )
    return {
        "method": "Synthetic Control Method (Abadie et al.)",
        "analysis": result
    }

@app.post("/instrumental-variables")
def run_iv_regression(data: IVRequest):
    # Validación simple de longitud
    if not (len(data.outcome_y) == len(data.endogenous_x) == len(data.instrument_z)):
        return {"error": "All series must have the same length"}
        
    result = CausalInference.instrumental_variables(
        data.outcome_y,
        data.endogenous_x,
        data.instrument_z
    )
    return {
        "method": "Two-Stage Least Squares (2SLS)",
        "result": result
    }

@app.get("/health")
def health():
    return {"status": "Causal Engine Operational", "modules": ["SCM", "IV-2SLS"]}
