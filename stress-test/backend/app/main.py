"""
FastAPI Main Application - Institutional Stress Test
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import simulations

app = FastAPI(
    title="Institutional Stress Test API",
    description="""
    ## B2B Consulting Tool for Process Optimization
    
    Uses Dark Agency agent simulation to identify bottlenecks in 
    organizational processes.
    
    ### How it works:
    1. Upload your process map (JSON/BPMN)
    2. We simulate Dark Agents vs Normal Agents navigating your process
    3. Where Dark Agents bypass rules most = Your bottlenecks
    
    ### Key Insight:
    *"Dark Agents find the friction points that slow down your best employees"*
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

app.include_router(simulations.router, prefix="/api/v1", tags=["Simulations"])


@app.get("/")
async def root():
    return {
        "name": "Institutional Stress Test API",
        "version": "1.0.0",
        "tagline": "Find what's slowing down your best employees",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
