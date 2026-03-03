"""
Database Models for Maverick Hunter
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from app.models.database import Base


class AssessmentStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class CandidateClassification(str, enum.Enum):
    MAVERICK = "MAVERICK"
    PERFORMER = "PERFORMER"
    RELIABLE = "RELIABLE"
    MONITOR = "MONITOR"
    RISK = "RISK"


class Company(Base):
    __tablename__ = "companies"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    api_key = Column(String(64), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessments = relationship("Assessment", back_populates="company")


class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessments = relationship("Assessment", back_populates="candidate")


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    
    status = Column(SQLEnum(AssessmentStatus), default=AssessmentStatus.PENDING)
    access_token = Column(String(64), unique=True)  # For candidate access
    
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="assessments")
    company = relationship("Company", back_populates="assessments")
    responses = relationship("Response", back_populates="assessment")
    result = relationship("Result", back_populates="assessment", uselist=False)


class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    
    item_code = Column(String(20), nullable=False)
    response = Column(Integer, nullable=False)  # 1-5 Likert
    response_time_ms = Column(Integer)  # Time to answer
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessment = relationship("Assessment", back_populates="responses")


class Result(Base):
    __tablename__ = "results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), unique=True, nullable=False)
    
    # Raw construct scores
    narcissism = Column(Float)
    machiavellianism = Column(Float)
    psychopathy = Column(Float)
    sadism = Column(Float)
    vigilance = Column(Float)
    psycap = Column(Float)
    
    # Bifactor outputs
    g_factor = Column(Float)
    s_agency = Column(Float)
    
    # Classification
    classification = Column(SQLEnum(CandidateClassification))
    confidence = Column(Float)
    
    # Predictions
    eib_prediction = Column(Float)
    cwb_o_risk = Column(Float)
    cwb_i_risk = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessment = relationship("Assessment", back_populates="result")