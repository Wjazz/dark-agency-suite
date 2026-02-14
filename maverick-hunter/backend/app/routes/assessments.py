"""
Assessment Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
import secrets
from datetime import datetime

from app.models.database import get_db
from app.models.schemas import Assessment, Candidate, Company, Response, Result, AssessmentStatus
from app.core.assessment import ALL_ITEMS, calculate_all_scores
from app.core.bifactor import PsychometricScores, analyze_candidate

router = APIRouter()


# Pydantic Schemas
class AssessmentCreate(BaseModel):
    candidate_email: EmailStr
    candidate_name: Optional[str] = None
    company_id: UUID


class AssessmentResponse(BaseModel):
    id: UUID
    status: str
    access_token: str
    candidate_email: str
    
    model_config = ConfigDict(from_attributes=True)


class ItemResponse(BaseModel):
    item_code: str
    response: int  # 1-5
    response_time_ms: Optional[int] = None


class SubmitResponses(BaseModel):
    responses: List[ItemResponse]


class AssessmentItem(BaseModel):
    code: str
    text: str
    text_es: str
    construct: str


class ResultResponse(BaseModel):
    classification: str
    semaphore_color: str
    confidence: float
    g_factor: float
    s_agency: float
    eib_prediction: float
    cwb_o_risk: float
    cwb_i_risk: float
    recommendation: str


# Routes
@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(data: AssessmentCreate, db: Session = Depends(get_db)):
    """
    Create a new assessment for a candidate
    
    Returns an access token for the candidate to complete the assessment.
    """
    # Get or create candidate
    candidate = db.query(Candidate).filter(Candidate.email == data.candidate_email).first()
    if not candidate:
        candidate = Candidate(email=data.candidate_email, name=data.candidate_name)
        db.add(candidate)
        db.flush()
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == data.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Create assessment
    assessment = Assessment(
        candidate_id=candidate.id,
        company_id=company.id,
        access_token=secrets.token_urlsafe(32)
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return AssessmentResponse(
        id=assessment.id,
        status=assessment.status.value,
        access_token=assessment.access_token,
        candidate_email=candidate.email
    )


@router.get("/{token}/items", response_model=List[AssessmentItem])
async def get_assessment_items(token: str, db: Session = Depends(get_db)):
    """
    Get assessment items for a candidate
    
    Uses the access token to authenticate.
    """
    assessment = db.query(Assessment).filter(Assessment.access_token == token).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status == AssessmentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Assessment already completed")
    
    # Mark as in progress
    if assessment.status == AssessmentStatus.PENDING:
        assessment.status = AssessmentStatus.IN_PROGRESS
        assessment.started_at = datetime.utcnow()
        db.commit()
    
    return [
        AssessmentItem(
            code=item.code,
            text=item.text,
            text_es=item.text_es,
            construct=item.construct.value
        )
        for item in ALL_ITEMS
    ]


@router.post("/{token}/submit", response_model=ResultResponse)
async def submit_assessment(token: str, data: SubmitResponses, db: Session = Depends(get_db)):
    """
    Submit assessment responses and get classification result
    """
    assessment = db.query(Assessment).filter(Assessment.access_token == token).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status == AssessmentStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Assessment already completed")
    
    # Save responses
    for item_resp in data.responses:
        response = Response(
            assessment_id=assessment.id,
            item_code=item_resp.item_code,
            response=item_resp.response,
            response_time_ms=item_resp.response_time_ms
        )
        db.add(response)
    
    # Calculate scores
    responses_dict = {r.item_code: r.response for r in data.responses}
    scores = calculate_all_scores(responses_dict)
    
    # Run Bifactor analysis
    psycho_scores = PsychometricScores(
        narcissism=scores["narcissism"],
        machiavellianism=scores["machiavellianism"],
        psychopathy=scores["psychopathy"],
        sadism=scores["sadism"],
        vigilance=scores["vigilance"],
        psycap=scores["psycap"]
    )
    
    result = analyze_candidate(psycho_scores)
    
    # Save result
    db_result = Result(
        assessment_id=assessment.id,
        narcissism=scores["narcissism"],
        machiavellianism=scores["machiavellianism"],
        psychopathy=scores["psychopathy"],
        sadism=scores["sadism"],
        vigilance=scores["vigilance"],
        psycap=scores["psycap"],
        g_factor=result.g_factor,
        s_agency=result.s_agency,
        classification=result.classification.value,
        confidence=result.confidence,
        eib_prediction=result.eib_prediction,
        cwb_o_risk=result.cwb_o_risk,
        cwb_i_risk=result.cwb_i_risk
    )
    db.add(db_result)
    
    # Mark assessment complete
    assessment.status = AssessmentStatus.COMPLETED
    assessment.completed_at = datetime.utcnow()
    
    db.commit()
    
    return ResultResponse(
        classification=result.classification.value,
        semaphore_color=result.semaphore_color,
        confidence=result.confidence,
        g_factor=result.g_factor,
        s_agency=result.s_agency,
        eib_prediction=result.eib_prediction,
        cwb_o_risk=result.cwb_o_risk,
        cwb_i_risk=result.cwb_i_risk,
        recommendation=result.hire_recommendation
    )


@router.get("/{assessment_id}", response_model=dict)
async def get_assessment_status(assessment_id: UUID, db: Session = Depends(get_db)):
    """Get assessment status"""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return {
        "id": str(assessment.id),
        "status": assessment.status.value,
        "started_at": assessment.started_at,
        "completed_at": assessment.completed_at
    }
