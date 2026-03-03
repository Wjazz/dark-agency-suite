"""
Results Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.models.database import get_db
from app.models.schemas import Result, Assessment

router = APIRouter()


class ResultDetail(BaseModel):
    id: UUID
    assessment_id: UUID
    
    # Scores
    narcissism: float
    machiavellianism: float
    psychopathy: float
    sadism: float
    vigilance: float
    psycap: float
    
    # Bifactor
    g_factor: float
    s_agency: float
    
    # Classification
    classification: str
    confidence: float
    
    # Predictions
    eib_prediction: float
    cwb_o_risk: float
    cwb_i_risk: float
    
    model_config = ConfigDict(from_attributes=True)


@router.get("/assessment/{assessment_id}", response_model=ResultDetail)
async def get_result_by_assessment(assessment_id: UUID, db: Session = Depends(get_db)):
    """Get result for a specific assessment"""
    result = db.query(Result).filter(Result.assessment_id == assessment_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return ResultDetail(
        id=result.id,
        assessment_id=result.assessment_id,
        narcissism=result.narcissism,
        machiavellianism=result.machiavellianism,
        psychopathy=result.psychopathy,
        sadism=result.sadism,
        vigilance=result.vigilance,
        psycap=result.psycap,
        g_factor=result.g_factor,
        s_agency=result.s_agency,
        classification=result.classification,
        confidence=result.confidence,
        eib_prediction=result.eib_prediction,
        cwb_o_risk=result.cwb_o_risk,
        cwb_i_risk=result.cwb_i_risk
    )


@router.get("/company/{company_id}/dashboard", response_model=dict)
async def get_company_dashboard(company_id: UUID, db: Session = Depends(get_db)):
    """Get aggregated results dashboard for a company"""
    results = db.query(Result).join(Assessment).filter(
        Assessment.company_id == company_id
    ).all()
    
    if not results:
        return {
            "total_assessments": 0,
            "classification_breakdown": {},
            "avg_g_factor": 0,
            "avg_s_agency": 0
        }
    
    # Count by classification
    breakdown = {}
    total_g = 0
    total_s = 0
    
    for r in results:
        cls = r.classification
        breakdown[cls] = breakdown.get(cls, 0) + 1
        total_g += r.g_factor
        total_s += r.s_agency
    
    return {
        "total_assessments": len(results),
        "classification_breakdown": breakdown,
        "avg_g_factor": round(total_g / len(results), 4),
        "avg_s_agency": round(total_s / len(results), 4),
        "maverick_count": breakdown.get("MAVERICK", 0),
        "risk_count": breakdown.get("RISK", 0)
    }
