"""
FastAPI Main Application - Founder Risk Assessment AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import assessments

app = FastAPI(
    title="Founder Risk Assessment AI",
    description="""
    ## Fintech/VC Tool for Emerging Market Founder Evaluation
    
    Uses the **IVR (Institutional Void Readiness)** algorithm to evaluate
    startup founders for their ability to navigate chaotic markets.
    
    ### Key Insight
    In Latam, Africa, and SEA, a "good and obedient" founder fails.
    You need a founder with **Dark Agency** to navigate corruption,
    bureaucracy, and informality - without being a criminal.
    
    ### Classification System
    - 🔵 **HIGH_POTENTIAL_MAVERICK**: Ideal for chaotic markets
    - 🟢 **ADAPTABLE_INNOVATOR**: Good potential
    - 🟡 **STRUCTURED_OPERATOR**: Better for stable markets
    - 🟠 **RED_FLAG_MONITOR**: Needs due diligence
    - 🔴 **CRIMINAL_RISK**: Do not invest
    
    ### IVR Formula
    ```
    IVR = 0.35×S_Agency + 0.25×VEE + 0.20×PsyCap + 0.15×POPS - 0.30×G
    ```
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessments.router, prefix="/api/v1", tags=["Assessments"])


@app.get("/")
async def root():
    return {
        "name": "Founder Risk Assessment AI",
        "version": "1.0.0",
        "tagline": "Predicting founder success in institutional voids",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
