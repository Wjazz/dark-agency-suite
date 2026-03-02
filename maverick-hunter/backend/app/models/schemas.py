from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
import uuid
import enum
from pydantic import BaseModel as PydanticBaseModel

# Importamos el GUID personalizado
from .database import Base, GUID

# --- Enums ---
class AssessmentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# --- Modelos SQLAlchemy (Base de Datos) ---

class Company(Base):
    __tablename__ = "companies"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    api_key = Column(String, unique=True)
    is_active = Column(Integer, default=1)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    results = relationship("AssessmentResult", back_populates="candidate")
    assessments = relationship("Assessment", back_populates="candidate")

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(GUID(), ForeignKey("candidates.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="assessments")

class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(GUID(), ForeignKey("candidates.id"))
    narcissism_score = Column(Float)
    machiavellianism_score = Column(Float)
    psychopathy_score = Column(Float)
    sadism_score = Column(Float)
    openness = Column(Float)
    conscientiousness = Column(Float)
    extraversion = Column(Float)
    agreeableness = Column(Float)
    neuroticism = Column(Float)
    risk_level = Column(String)
    raw_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="results")

# --- Alias para compatibilidad con código legacy ---
# Si tu código viejo busca "Result", le damos "AssessmentResult"
Result = AssessmentResult

# --- Modelos Pydantic (Validación API) ---
class Response(PydanticBaseModel):
    question_id: str
    answer_value: int
