# Institutional Stress Test 🏭

**B2B Consulting Tool for Process Optimization**

> *"Find what's slowing down your best employees"*

## What is This?

A simulation engine that uses **Dark Agency agents** to identify bottlenecks in organizational processes. Dark Agents - employees with high S_Agency - strategically bypass unnecessary bureaucracy. Where they transgress most = where your process has friction.

## How It Works

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  UPLOAD PROCESS  │────▶│  SIMULATE AGENTS │────▶│  BOTTLENECK      │
│  (JSON/BPMN)     │     │  Dark vs Normal  │     │  REPORT          │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Key Metrics

| Metric | Description |
|--------|-------------|
| **Transgression Rate** | How often Dark Agents bypass this node |
| **Efficiency Gap** | % faster Dark Agents complete vs Normal |
| **Bottleneck Severity** | Combined friction score (0-1) |
| **Recommendation** | ELIMINATE / STREAMLINE / ACCELERATE / MONITOR |

## Quick Start

```bash
cd ~/proyectos/stress-test/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/simulate` | Run simulation on process |
| GET | `/api/v1/samples` | List sample processes |
| GET | `/api/v1/samples/{id}` | Get sample process |
| POST | `/api/v1/quick-test/{id}` | Quick test sample |

## Example Output

```json
{
  "process_name": "Employee Onboarding",
  "efficiency_gap_percent": 34.5,
  "interpretation": "CRITICAL: Dark Agents complete 34.5% faster...",
  "bottlenecks": [
    {
      "node_name": "VP Final Approval",
      "severity": 0.82,
      "transgression_rate": 0.71,
      "recommendation": "ELIMINATE: This approval adds friction without value."
    }
  ]
}
```

## The Pitch

> *"My software uses AI agents to find which of your company's policies 
> are hindering innovation, by simulating the behavior of your smartest 
> employees."*

---

Based on thesis: *"Dark Agency in Institutional Voids"*
