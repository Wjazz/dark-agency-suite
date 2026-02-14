"""
Simulation Routes - Institutional Stress Test
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

from app.core.simulator import run_stress_test, BottleneckReport

router = APIRouter()


class ProcessInput(BaseModel):
    """Process map input"""
    process: Dict[str, Any]
    n_dark_agents: int = 20
    n_normal_agents: int = 50


class BottleneckResponse(BaseModel):
    node_id: str
    node_name: str
    severity: float
    transgression_rate: float
    avg_wait_time: float
    recommendation: str


class SimulationResponse(BaseModel):
    process_name: str
    total_ticks: int
    summary: Dict[str, Any]
    bottlenecks: List[BottleneckResponse]
    efficiency_gap_percent: float
    interpretation: str


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(data: ProcessInput):
    """
    Run stress test simulation on a process
    
    Upload your process map and see where Dark Agents find friction.
    """
    try:
        result = run_stress_test(
            data.process, 
            n_dark=data.n_dark_agents, 
            n_normal=data.n_normal_agents
        )
        
        summary = result.get_summary()
        bottlenecks = result.get_bottlenecks()
        
        efficiency_gap = summary['efficiency_gap'] * 100
        
        # Generate interpretation
        if efficiency_gap > 30:
            interpretation = f"CRITICAL: Dark Agents complete {efficiency_gap:.1f}% faster. Your process has severe bureaucratic friction hindering top performers."
        elif efficiency_gap > 15:
            interpretation = f"MODERATE: Dark Agents complete {efficiency_gap:.1f}% faster. Several approval points could be streamlined."
        elif efficiency_gap > 5:
            interpretation = f"MILD: Dark Agents complete {efficiency_gap:.1f}% faster. Minor optimization opportunities exist."
        else:
            interpretation = "HEALTHY: Minimal gap between agent types. Process is well-optimized."
        
        return SimulationResponse(
            process_name=result.process_name,
            total_ticks=result.total_ticks,
            summary=summary,
            bottlenecks=[
                BottleneckResponse(
                    node_id=b.node_id,
                    node_name=b.node_name,
                    severity=round(b.severity, 3),
                    transgression_rate=round(b.transgression_rate, 3),
                    avg_wait_time=round(b.avg_wait_time, 2),
                    recommendation=b.recommendation
                )
                for b in bottlenecks
            ],
            efficiency_gap_percent=round(efficiency_gap, 2),
            interpretation=interpretation
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/samples")
async def list_sample_processes():
    """List available sample processes for testing"""
    samples_dir = os.path.join(os.path.dirname(__file__), "../../sample_processes")
    
    # For demo, return hardcoded list
    return {
        "samples": [
            {
                "id": "onboarding",
                "name": "Employee Onboarding",
                "description": "HR onboarding with multiple approval gates",
                "nodes": 10,
                "approvals": 5
            },
            {
                "id": "purchase_requisition",
                "name": "Purchase Requisition",
                "description": "Procurement flow - notorious for bottlenecks",
                "nodes": 13,
                "approvals": 6
            }
        ]
    }


@router.get("/samples/{sample_id}")
async def get_sample_process(sample_id: str):
    """Get a sample process for testing"""
    samples = {
        "onboarding": {
            "name": "Employee Onboarding Process",
            "start": "start",
            "end": "end",
            "nodes": [
                {"id": "start", "name": "New Hire Request", "type": "start", "next": ["hr_review"]},
                {"id": "hr_review", "name": "HR Initial Review", "type": "approval", "wait_time": 3, "approval_probability": 0.95, "next": ["dept_approval"]},
                {"id": "dept_approval", "name": "Department Manager Approval", "type": "approval", "wait_time": 5, "approval_probability": 0.85, "next": ["budget_check"]},
                {"id": "budget_check", "name": "Budget Verification", "type": "approval", "wait_time": 8, "approval_probability": 0.75, "next": ["vp_approval"]},
                {"id": "vp_approval", "name": "VP Final Approval", "type": "approval", "wait_time": 10, "approval_probability": 0.90, "next": ["create_accounts"]},
                {"id": "create_accounts", "name": "Create System Accounts", "type": "task", "base_time": 2, "next": ["equipment_request"]},
                {"id": "equipment_request", "name": "Equipment Request", "type": "approval", "wait_time": 7, "approval_probability": 0.80, "next": ["access_cards"]},
                {"id": "access_cards", "name": "Access Card Creation", "type": "task", "base_time": 1, "next": ["orientation"]},
                {"id": "orientation", "name": "New Hire Orientation", "type": "task", "base_time": 3, "next": ["end"]},
                {"id": "end", "name": "Onboarding Complete", "type": "end", "next": []}
            ]
        },
        "purchase_requisition": {
            "name": "Purchase Requisition Process",
            "start": "start",
            "end": "end",
            "nodes": [
                {"id": "start", "name": "Purchase Request Created", "type": "start", "next": ["spec_review"]},
                {"id": "spec_review", "name": "Specs Review", "type": "task", "base_time": 2, "next": ["manager_approval"]},
                {"id": "manager_approval", "name": "Manager Approval", "type": "approval", "wait_time": 4, "approval_probability": 0.90, "next": ["finance_review"]},
                {"id": "finance_review", "name": "Finance Review", "type": "approval", "wait_time": 12, "approval_probability": 0.65, "next": ["cfo_approval"]},
                {"id": "cfo_approval", "name": "CFO Approval", "type": "approval", "wait_time": 15, "approval_probability": 0.85, "next": ["legal_review"]},
                {"id": "legal_review", "name": "Legal Review", "type": "approval", "wait_time": 10, "approval_probability": 0.75, "next": ["end"]},
                {"id": "end", "name": "Purchase Complete", "type": "end", "next": []}
            ]
        }
    }
    
    if sample_id not in samples:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    return samples[sample_id]


@router.post("/quick-test/{sample_id}")
async def quick_test(sample_id: str):
    """Run quick test on a sample process"""
    # Get sample
    sample = await get_sample_process(sample_id)
    
    # Run simulation
    return await run_simulation(ProcessInput(
        process=sample,
        n_dark_agents=15,
        n_normal_agents=40
    ))
