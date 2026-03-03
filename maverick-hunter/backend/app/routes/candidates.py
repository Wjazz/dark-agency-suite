"""
Candidates Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from app.models.database import get_db
from app.models.schemas import Candidate, Assessment

router = APIRouter()


class CandidateResponse(BaseModel):
    id: UUID
    email: str
    name: str | None
    assessment_count: int
    
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=List[CandidateResponse])
async def list_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all candidates"""
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return [
        CandidateResponse(
            id=c.id,
            email=c.email,
            name=c.name,
            assessment_count=len(c.assessments)
        )
        for c in candidates
    ]


@router.get("/{candidate_id}", response_model=dict)
async def get_candidate(candidate_id: UUID, db: Session = Depends(get_db)):
    """Get candidate details with all assessments"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return {
        "id": str(candidate.id),
        "email": candidate.email,
        "name": candidate.name,
        "created_at": candidate.created_at,
        "assessments": [
            {
                "id": str(a.id),
                "status": a.status.value,
                "company_id": str(a.company_id),
                "completed_at": a.completed_at
            }
            for a in candidate.assessments
        ]
    }
