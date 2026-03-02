"""
Maverick Hunter - FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import assessments, candidates, results
from app.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    init_db()
    yield
    # Shutdown


app = FastAPI(
    title="Maverick Hunter API",
    description="""
    ## HR Tech SaaS for Identifying Dark Innovators
    
    Based on Bifactor S-1 Model from thesis:
    "Dark Agency in Institutional Voids"
    
    ### Classification System
    - 🔵 **MAVERICK**: High S_Agency, Low G - Innovation/Leadership roles
    - 🟢 **PERFORMER**: Moderate S_Agency, Low G - High growth potential
    - 🟡 **RELIABLE**: Low S_Agency, Low G - Structured roles
    - 🟠 **MONITOR**: High S_Agency, Moderate G - Needs coaching
    - 🔴 **RISK**: High G - Do not hire
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(candidates.router, prefix="/api/v1/candidates", tags=["Candidates"])
app.include_router(results.router, prefix="/api/v1/results", tags=["Results"])


@app.get("/")
async def root():
    return {
        "name": "Maverick Hunter API",
        "version": "1.0.0",
        "tagline": "Hire the people who break the right rules",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
