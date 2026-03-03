# Maverick Hunter 🎯

**HR Tech SaaS for Identifying Dark Innovators**

> *"Hire the people who break the right rules"*

## What is This?

Traditional psychometric tests reject candidates who seem "conflictive." But research shows that **Dark Innovators** — people who strategically transgress rules to drive innovation — are often mislabeled as troublemakers.

Using the **Bifactor S-1 Model**, Maverick Hunter distinguishes between:
- **S_Agency** (Dark Agency): Strategic rule-breaking that drives innovation ✅
- **G Factor**: Destructive toxicity that harms others ❌

## Classification System

| Color | Type | Description | Recommendation |
|-------|------|-------------|----------------|
| 🔵 Cyan | **MAVERICK** | High S_Agency, Low G | Hire for innovation/leadership |
| 🟢 Green | **PERFORMER** | Moderate S_Agency, Low G | Hire, high growth potential |
| 🟡 Yellow | **RELIABLE** | Low S_Agency, Low G | Hire for structured roles |
| 🟠 Orange | **MONITOR** | High S_Agency, Moderate G | Hire with coaching |
| 🔴 Red | **RISK** | High G | Do not hire |

## Quick Start

### Option 1: Docker (Recommended)

```bash
cd ~/proyectos/maverick-hunter
docker-compose up --build
```

Access:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assessments/` | Create new assessment |
| GET | `/api/v1/assessments/{token}/items` | Get test items |
| POST | `/api/v1/assessments/{token}/submit` | Submit and get result |
| GET | `/api/v1/results/company/{id}/dashboard` | Company dashboard |

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + Vite
- **Core Engine**: Bifactor S-1 Model (Python)
- **Deploy**: Docker Compose

## The Thesis

Based on research: *"Dark Agency in Institutional Voids"*

The core insight: In chaotic environments (institutional voids), some employees use "dark" traits strategically to innovate — **not** to harm. The Bifactor S-1 model mathematically separates productive darkness (S_Agency) from destructive darkness (G Factor).

---

*"La rebeldía calculada es rentabilidad"*
