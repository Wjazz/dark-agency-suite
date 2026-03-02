# Founder Risk Assessment AI 💰

**Fintech/VC Tool for Emerging Market Founder Evaluation**

> *"Predicting founder success in institutional voids"*

## The Problem

VCs in LatAm, Africa, and SEA have fear of investing because the market is chaotic (Institutional Voids). But traditional founder assessments fail here because:

- A "good and obedient" founder **fails** in chaotic markets
- You need a founder with high **Dark Agency** to survive corruption, bureaucracy, and informality
- But you also need to filter out actual criminals (high G-factor)

## The Solution: IVR Score

**Institutional Void Readiness (IVR)** measures a founder's ability to navigate chaos:

```
IVR = (0.35 × S_Agency) + (0.25 × VEE) + (0.20 × PsyCap) 
    + (0.15 × POPS) - (0.30 × G)
```

## Classification System

| Color | Type | Market Fit | Recommendation |
|-------|------|------------|----------------|
| 🔵 Cyan | **HIGH_POTENTIAL_MAVERICK** | Emerging | STRONG INVEST |
| 🟢 Green | **ADAPTABLE_INNOVATOR** | Mixed | INVEST |
| 🟡 Yellow | **STRUCTURED_OPERATOR** | Developed | CONDITIONAL |
| 🟠 Orange | **RED_FLAG_MONITOR** | - | PASS |
| 🔴 Red | **CRIMINAL_RISK** | - | REJECT |

## Quick Start

```bash
cd ~/proyectos/founder-risk-ai/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assess` | Full assessment with detailed profile |
| POST | `/api/v1/quick-assess` | Quick 1-5 scale assessment |
| GET | `/api/v1/demo/maria-garcia` | Demo: María García assessment |
| GET | `/api/v1/markets` | Get market chaos indices |

## Example Response

```json
{
  "founder": "María García",
  "startup": "FinTech Latina",
  "ivr_score": 0.78,
  "classification": "HIGH_POTENTIAL_MAVERICK",
  "recommendation": "STRONG_INVEST",
  "risk_flags": [],
  "narrative": "High-potential founder with exceptional 
                institutional navigation capability..."
}
```

## The Pitch

> *"Founder screening for emerging markets. My AI predicts which
> founders have the 'stomach' to navigate institutional voids
> without becoming criminals. Dark Agency that builds, not destroys."*

---

Based on thesis: *"Dark Agency in Institutional Voids"*
