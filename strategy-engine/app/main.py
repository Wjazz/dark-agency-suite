from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.core.nash_equilibrium import AuctionStrategist

app = FastAPI(
    title="Dark Agency Strategy Engine",
    version="1.0.0",
    description="Motor de Teoría de Juegos y Decisiones Estratégicas (Nash/Bayes)"
)

class AuctionRequest(BaseModel):
    valuation: float = Field(..., description="Cuánto valoras el proyecto/objeto", gt=0)
    competitors: int = Field(..., description="Número estimado de rivales", gt=1)
    risk_profile: str = Field("neutral", description="neutral, averse, lover")

@app.post("/optimize-bid")
def calculate_bid(request: AuctionRequest):
    # Mapeo de perfil de riesgo a parámetro matemático
    risk_map = {"neutral": 0.0, "averse": 0.5, "lover": -0.2}
    risk_val = risk_map.get(request.risk_profile, 0.0)
    
    strategy = AuctionStrategist.optimal_bid_first_price(
        request.valuation, 
        request.competitors, 
        risk_val
    )
    
    return {
        "inputs": request.dict(),
        "strategy": "Bayesian Nash Equilibrium (First Price)",
        "recommendation": strategy
    }

@app.get("/health")
def health():
    return {"status": "Strategy Engine Ready", "theory": "Game Theory Enabled"}
