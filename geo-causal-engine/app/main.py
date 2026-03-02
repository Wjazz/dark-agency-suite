from fastapi import FastAPI
from app.models.schemas import GeoPsychometricInput
from app.core.spatial_metrics import SpatialStressCalculator
from app.core.bayesian_model import PoliticalInferenceEngine # (Tu lógica causal)

app = FastAPI(
    title="Geo-Causal Engine",
    version="1.0.0",
    description="Motor Hexagonal de Inferencia: Teledetección Geoespacial + Psicometría"
)

@app.post("/infer-political-structure")
def infer_structure(data: GeoPsychometricInput):
    # 1. Transformación de la capa física (Teledetección)
    env_stress = SpatialStressCalculator.calculate_environmental_stress(
        ndvi=data.ndvi_mean, 
        lst=data.lst_mean_celsius
    )
    
    # 2. Inferencia Causal (Hexágono central puro)
    # Alta extraversión + Alto estrés geográfico = Probabilidad de Caudillismo (Patria)
    # Alta responsabilidad + Alto estrés geográfico = Probabilidad de Institucionalidad (Nación)
    
    nation_score = (data.conscientiousness_agg * 1.5) + (env_stress * 0.5) - data.extraversion_agg
    patria_score = (data.extraversion_agg * 1.5) + (env_stress * 0.8) - data.conscientiousness_agg
    
    # Función Softmax simplificada para probabilidad
    import numpy as np
    total = np.exp(nation_score) + np.exp(patria_score)
    prob_nation = np.exp(nation_score) / total
    prob_patria = np.exp(patria_score) / total
    
    synthesis = "Nación (Institucional)" if prob_nation > prob_patria else "Patria (Caudillista/Folclórica)"

    return {
        "telemetry_inputs": data.dict(),
        "calculated_environmental_stress": env_stress,
        "causal_inference": {
            "probability_nation": round(prob_nation, 4),
            "probability_patria": round(prob_patria, 4)
        },
        "emergent_synthesis": synthesis
    }

@app.get("/health")
def health_check():
    return {"status": "Geo-Causal Engine Operativo. Sensores calibrados."}
