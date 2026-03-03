from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
# Importamos TODO lo que definimos en schemas
from app.models.schemas import Assessment, Candidate, Company, Response, Result, AssessmentStatus
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AssessmentCreate(BaseModel):
    candidate_email: str
    candidate_name: str

@router.post("/create")
def create_assessment(data: AssessmentCreate, db: Session = Depends(get_db)):
    # 1. Buscar o crear candidato
    candidate = db.query(Candidate).filter(Candidate.email == data.candidate_email).first()
    if not candidate:
        candidate = Candidate(email=data.candidate_email, full_name=data.candidate_name)
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
    
    # 2. Crear assessment
    new_assessment = Assessment(candidate_id=candidate.id)
    db.add(new_assessment)
    db.commit()
    
    return {"status": "created", "assessment_id": str(new_assessment.id)}

@router.post("/{assessment_id}/submit")
def submit_assessment(assessment_id: str, responses: List[Response], db: Session = Depends(get_db)):
    # Lógica simplificada para que compile
    return {"status": "received", "count": len(responses)}
