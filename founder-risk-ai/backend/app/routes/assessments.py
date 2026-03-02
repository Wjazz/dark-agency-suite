"""
Assessment Routes - Founder Risk AI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.ivr_engine import FounderProfile, assess_founder, IVRResult

router = APIRouter()


class FounderInput(BaseModel):
    """Input for founder assessment"""
    founder_name: str
    startup_name: str
    
    # Dark Tetrad scores (0-1)
    narcissism: float = Field(ge=0, le=1)
    machiavellianism: float = Field(ge=0, le=1)
    psychopathy: float = Field(ge=0, le=1)
    sadism: float = Field(ge=0, le=1)
    
    # Additional constructs
    vigilance: float = Field(ge=0, le=1, default=0.5)
    psycap: float = Field(ge=0, le=1, default=0.5)
    pops: float = Field(ge=0, le=1, default=0.5)
    
    # Market context
    market_chaos: float = Field(ge=0, le=1, default=0.6)
    regulatory_burden: float = Field(ge=0, le=1, default=0.5)
    corruption_index: float = Field(ge=0, le=1, default=0.5)


class AssessmentResponse(BaseModel):
    founder_name: str
    startup_name: str
    
    # Core scores
    ivr_score: float
    g_factor: float
    s_agency: float
    
    # Classification
    classification: str
    semaphore_color: str
    recommendation: str
    confidence: float
    
    # Risk analysis
    risk_flags: List[str]
    
    # Narrative for partners
    narrative: str


class QuickAssessInput(BaseModel):
    """Simplified input for quick assessment"""
    founder_name: str
    startup_name: str
    market: str = "latam"  # latam, africa, sea, developed
    
    # Simplified 1-5 scale answers
    ambitious: int = Field(ge=1, le=5, description="How ambitious/driven")
    strategic: int = Field(ge=1, le=5, description="How strategic/calculating")
    rule_breaking: int = Field(ge=1, le=5, description="Willingness to bend rules")
    empathy: int = Field(ge=1, le=5, description="Empathy for others (inverse)")
    resilient: int = Field(ge=1, le=5, description="Resilience to setbacks")
    politically_savvy: int = Field(ge=1, le=5, description="Political awareness")
    opportunity_alert: int = Field(ge=1, le=5, description="Alertness to opportunities")


@router.post("/assess", response_model=AssessmentResponse)
async def assess(data: FounderInput):
    """
    Full founder assessment with detailed profile
    
    Provide complete psychometric scores for detailed analysis.
    """
    profile = FounderProfile(
        narcissism=data.narcissism,
        machiavellianism=data.machiavellianism,
        psychopathy=data.psychopathy,
        sadism=data.sadism,
        vigilance=data.vigilance,
        psycap=data.psycap,
        pops=data.pops,
        market_chaos=data.market_chaos,
        regulatory_burden=data.regulatory_burden,
        corruption_index=data.corruption_index
    )
    
    result = assess_founder(profile)
    
    return AssessmentResponse(
        founder_name=data.founder_name,
        startup_name=data.startup_name,
        ivr_score=result.ivr_score,
        g_factor=result.g_factor,
        s_agency=result.s_agency,
        classification=result.classification.value,
        semaphore_color=result.semaphore_color,
        recommendation=result.recommendation.value,
        confidence=result.confidence,
        risk_flags=result.risk_flags,
        narrative=result.narrative
    )


@router.post("/quick-assess", response_model=AssessmentResponse)
async def quick_assess(data: QuickAssessInput):
    """
    Quick assessment using simplified 1-5 scale
    
    For rapid screening during pitch meetings.
    """
    # Convert 1-5 to 0-1
    def normalize(val: int) -> float:
        return (val - 1) / 4.0
    
    # Map simplified inputs to full profile
    narcissism = normalize(data.ambitious)
    machiavellianism = normalize(data.strategic)
    psychopathy = normalize(data.rule_breaking) * 0.6  # Scale down
    sadism = max(0, normalize(5 - data.empathy) * 0.3)  # Low weight
    
    # Market chaos by region
    market_chaos = {
        "latam": 0.70,
        "africa": 0.80,
        "sea": 0.65,
        "developed": 0.35
    }.get(data.market, 0.5)
    
    profile = FounderProfile(
        narcissism=narcissism,
        machiavellianism=machiavellianism,
        psychopathy=psychopathy,
        sadism=sadism,
        vigilance=normalize(data.opportunity_alert),
        psycap=normalize(data.resilient),
        pops=normalize(data.politically_savvy),
        market_chaos=market_chaos,
        regulatory_burden=market_chaos * 0.8,
        corruption_index=market_chaos * 0.7
    )
    
    result = assess_founder(profile)
    
    return AssessmentResponse(
        founder_name=data.founder_name,
        startup_name=data.startup_name,
        ivr_score=result.ivr_score,
        g_factor=result.g_factor,
        s_agency=result.s_agency,
        classification=result.classification.value,
        semaphore_color=result.semaphore_color,
        recommendation=result.recommendation.value,
        confidence=result.confidence * 0.9,  # Slightly lower for quick
        risk_flags=result.risk_flags,
        narrative=result.narrative
    )


@router.get("/demo/maria-garcia")
async def demo_assessment():
    """Demo assessment - María García, FinTech Latina founder"""
    profile = FounderProfile(
        narcissism=0.72,
        machiavellianism=0.78,
        psychopathy=0.25,
        sadism=0.12,
        vigilance=0.85,
        psycap=0.80,
        pops=0.75,
        market_chaos=0.75,  # LatAm
        regulatory_burden=0.70,
        corruption_index=0.65
    )
    
    result = assess_founder(profile)
    
    return {
        "founder": "María García",
        "startup": "FinTech Latina",
        "ivr_score": result.ivr_score,
        "g_factor": result.g_factor,
        "s_agency": result.s_agency,
        "classification": result.classification.value,
        "recommendation": result.recommendation.value,
        "risk_flags": result.risk_flags,
        "narrative": result.narrative
    }


@router.get("/markets")
async def get_markets():
    """Get predefined market chaos indices"""
    return {
        "markets": [
            {"id": "latam", "name": "Latin America", "chaos_index": 0.70},
            {"id": "africa", "name": "Sub-Saharan Africa", "chaos_index": 0.80},
            {"id": "sea", "name": "Southeast Asia", "chaos_index": 0.65},
            {"id": "mena", "name": "Middle East & North Africa", "chaos_index": 0.60},
            {"id": "india", "name": "India", "chaos_index": 0.55},
            {"id": "developed", "name": "Developed Markets", "chaos_index": 0.35}
        ]
    }
