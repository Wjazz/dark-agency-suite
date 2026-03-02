from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.financial_risk import DarkRiskEngine

router = APIRouter()

# --- Pydantic Models ---
class PortfolioRequest(BaseModel):
    portfolio_value: float = Field(..., description="Total value of assets in USD", gt=0)
    annual_volatility: float = Field(..., description="Annualized volatility (e.g. 0.15 for 15%)", gt=0, le=1.0)
    scenario: str = Field(..., description="Scenario: 'BAU', 'Net_Zero_2030', 'Climate_Disorder'")

class StressResponse(BaseModel):
    status: str
    scenario_analysis: dict

# --- Logic ---
@router.post("/run-climate-stress", response_model=StressResponse)
async def run_stress_test(request: PortfolioRequest):
    # 1. Initialize Engine
    engine = DarkRiskEngine(confidence_level=0.99)
    
    # 2. Define Scenarios (Based on NGFS / Basel definitions)
    scenarios = {
        "BAU": 1.0,               # No change
        "Net_Zero_2030": 1.35,    # Transition risk increases volatility by 35%
        "Climate_Disorder": 2.80  # Physical + Transition risk spikes volatility by 180%
    }
    
    if request.scenario not in scenarios:
        raise HTTPException(status_code=400, detail=f"Scenario must be one of: {list(scenarios.keys())}")
    
    shock = scenarios[request.scenario]
    
    # 3. Execute Calculation
    result = engine.stress_test_climate_scenario(
        request.portfolio_value,
        request.annual_volatility,
        shock
    )
    
    return {
        "status": "success",
        "scenario_analysis": result
    }
