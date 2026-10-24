# Task 5 — HumanCheck: Local Writing Pattern Analyzer

HumanCheck is a privacy-first writing analysis prototype. Paste text to receive an **AI-like vs human-like writing-pattern estimate**, sentence-level pattern flags, and a readable explanation. The application is designed to run locally and does not require a paid API key.

> **Important limitation:** Text alone cannot reliably prove who wrote it. The percentages shown are model scores normalized for display, not calibrated probabilities or proof of authorship. Human writing can be flagged as AI-like, and AI-generated writing can look human. Do not use this tool as the sole basis for academic, employment, disciplinary, or other high-stakes decisions.

## Features

- React + Vite responsive interface.
- FastAPI backend with a locally downloaded Hugging Face text-classification model.
- No OpenAI/Gemini/Claude API key and no external inference API.
- Sentence-level pattern inspection and readable metrics.
- Transparent fallback analysis if the model cannot be loaded.
- Local-only processing by default; text is not saved by the app.
- Basic automated tests for text metrics and API validation.

## Architecture

- **Frontend:** React, Vite, CSS.
- **Backend:** Python 3.10+, FastAPI, Uvicorn.
- **ML:** Hugging Face Transformers + PyTorch. Default model: `openai-community/roberta-base-openai-detector`. Model weights are downloaded from Hugging Face on the first model-backed run and cached locally.
- **Fallback:** Deterministic writing-pattern heuristics, clearly identified as a fallback rather than a trained detector.

## Run locally

### 1. Backend

From the repository root:

```bash
cd Task-5/backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

On first analysis, Transformers may download the model weights. This needs an internet connection once, disk space, and enough RAM. After the model is cached, inference runs locally. If the model is unavailable, the API can use the built-in heuristic fallback; the result will be labelled accordingly.

### 2. Frontend

Open a second terminal:

```bash
cd Task-5/frontend
npm install
npm run dev
```

Visit the local URL printed by Vite (normally http://localhost:5173). The frontend calls the backend at http://127.0.0.1:8000.

### Optional environment variables

- `HUMANCHECK_MODEL`: Hugging Face model ID (default shown above).
- `HUMANCHECK_ALLOW_HEURISTIC_FALLBACK`: set to `true` to allow heuristic fallback (default: true).
- `VITE_API_URL`: backend base URL for the frontend (default: http://127.0.0.1:8000).

## API

- `GET /health` — API and model status.
- `POST /analyze` — JSON body: `{"text":"..."}`.
- `GET /docs` — interactive local API docs.

## What the scores mean

The model returns class scores for its training distribution. HumanCheck displays the relative AI-like and human-like score for a simple comparison. They are **not calibrated authorship probabilities**. Very short text, non-English text, code, quotations, edited text, and domains unlike the model's training data can produce unreliable results. Sentence-level flags are explanatory pattern cues, not proof that a sentence was AI-written.

## Testing

```bash
cd Task-5/backend
pip install -r requirements.txt
pytest -q
```

## Responsible use

- Treat results as a prompt for review, not a verdict.
- Preserve drafts, notes, version history, and source records when authorship matters.
- Avoid uploading private or sensitive content to a hosted service. This prototype is intended for local use.
- Review the model card and licence for the chosen model before redistribution or production deployment.
