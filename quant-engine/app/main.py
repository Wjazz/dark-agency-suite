from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.core.pricing_models import NeuralPricer, BlackScholesMath
import time

app = FastAPI(
    title="Quant Engine: Neural Derivatives Pricing",
    version="1.0.0",
    description="Motor de valuación híbrido: Fórmula Cerrada vs Red Neuronal"
)

# Instancia global (Singlenton)
pricer = NeuralPricer()

# Entrenar al inicio (Cold Start)
@app.on_event("startup")
def startup_event():
    pricer.train_dummy()

class OptionParams(BaseModel):
    S: float = Field(..., description="Precio Spot del activo", gt=0)
    K: float = Field(..., description="Precio Strike", gt=0)
    T: float = Field(..., description="Tiempo en años", gt=0)
    r: float = Field(0.05, description="Tasa libre de riesgo")
    sigma: float = Field(0.2, description="Volatilidad implícita")

@app.post("/price-option")
def price_option(params: OptionParams):
    start_time = time.time()
    
    # 1. Benchmark (Matemática Pura)
    bs_price = BlackScholesMath.call_price(
        params.S, params.K, params.T, params.r, params.sigma
    )
    
    # 2. IA Prediction
    ai_price = pricer.predict(
        params.S, params.K, params.T, params.r, params.sigma
    )
    
    inference_time = time.time() - start_time
    
    error = abs(bs_price - ai_price)
    
    return {
        "prices": {
            "black_scholes_classic": round(bs_price, 4),
            "neural_network_estimate": round(ai_price, 4)
        },
        "accuracy_analysis": {
            "absolute_error": round(error, 4),
            "percentage_error": round((error/bs_price)*100, 2) if bs_price > 0 else 0.0
        },
        "performance_ms": round(inference_time * 1000, 2)
    }

@app.get("/health")
def health():
    return {"status": "operational", "trained": pricer.is_trained}
