# AgenticBI — Local Multi-Agent Analyst & PPT Builder

AgenticBI turns a local CSV file into a data-quality report, evidence-backed findings, and a styled PowerPoint presentation. It requires no paid inference API.

## Features
- CSV profiling: missing values, duplicate rows, data types and previews.
- Fixed, auditable pandas analysis; the model never executes generated Python.
- Optional local Ollama model to phrase already-computed findings.
- Isolation Forest anomaly detection when numeric data is suitable.
- PowerPoint export with findings, quality checks, numeric overview and limitations.
- FastAPI backend and React/Vite frontend.

## Local setup
Requirements: Python 3.10+, Node.js 18+. Ollama is optional.

Backend (from repository root):
```bash
cd Task-6/AgenticBI/backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend, in another terminal:
```bash
cd Task-6/AgenticBI/frontend
npm install
npm run dev
```

Open the local URL shown by Vite. API docs are at http://127.0.0.1:8000/docs.

Optional local LLM:
```bash
ollama pull qwen2.5:7b
```
Set `OLLAMA_MODEL` if you use another model. If Ollama is not running, deterministic findings still work.

## API
- `GET /api/health`
- `POST /api/analyze` — CSV upload, JSON results
- `POST /api/report` — CSV upload, downloadable PPTX

## Workflow
Inspector → cleaning/profile stage → statistical analyst → optional local narrative → report builder → validation. These are orchestrated stages, not six separate models; this keeps the starter reliable and testable.

## Safety and limitations
- Never executes LLM-generated code. Data processing uses fixed Python functions.
- Uploaded CSVs are processed in memory and not saved to disk by the app.
- Anomaly flags are investigation leads, not proof of fraud or error.
- LLM narrative is a draft. Computed metrics are the source of truth.
- Validate business definitions and findings before acting on them.
- Upload limit: 15 MB and 50,000 rows.

Start with `backend/sample_data/sales_sample.csv` to test the workflow.