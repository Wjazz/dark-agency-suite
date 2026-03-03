from fastapi import FastAPI
from app.routes import simulations

app = FastAPI(
    title="Dark Agency Stress Test Engine",
    description="Microservice for Financial & Climate Risk Calculation",
    version="1.0.0"
)

app.include_router(simulations.router, prefix="/api/v1", tags=["Simulations"])

@app.get("/health")
def health_check():
    return {"status": "operational", "engine": "DarkRiskEngine v1"}
