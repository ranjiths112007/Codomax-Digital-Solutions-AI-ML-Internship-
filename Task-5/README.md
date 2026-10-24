# Task 5 — HumanCheck: Local Writing Pattern Analyzer

**Live frontend:** [Open HumanCheck on GitHub Pages](https://ranjiths112007.github.io/Codomax-Digital-Solutions-AI-ML-Internship-/)  
**Source code:** [Task-5 folder](https://github.com/ranjiths112007/Codomax-Digital-Solutions-AI-ML-Internship-/tree/main/Task-5)

HumanCheck is a writing-pattern analysis prototype. Paste text to receive an AI-like vs human-like writing-pattern estimate, sentence-level pattern flags, and a readable explanation. The project uses a React frontend and a Python FastAPI backend, without requiring a paid API key.

> **Important limitation:** Text alone cannot reliably prove who wrote it. The percentages shown are model scores normalized for display, not calibrated probabilities or proof of authorship. Human writing can be flagged as AI-like, and AI-generated writing can look human. Do not use this tool as the sole basis for academic, employment, disciplinary, or other high-stakes decisions.

## Features

- Responsive React + Vite interface.
- FastAPI backend with a locally downloaded Hugging Face text-classification model.
- No paid OpenAI, Gemini, Claude, or other inference API key.
- Sentence-level pattern inspection and readable metrics.
- Transparent heuristic fallback if the model cannot be loaded.
- Local processing by default; the app does not save submitted text.
- Automated tests for text metrics and API validation.

## Project structure

```text
Task-5/
├── README.md
├── .gitignore
├── backend/
│   ├── main.py
│   ├── detector.py
│   ├── requirements.txt
│   └── test_detector.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        └── index.css
```

## Technology

- **Frontend:** React, Vite, CSS.
- **Backend:** Python 3.10+, FastAPI, Uvicorn.
- **ML:** Hugging Face Transformers + PyTorch. Default model: `openai-community/roberta-base-openai-detector`.
- **Fallback:** Deterministic writing-pattern heuristics, identified as a fallback rather than a trained detector.

The model weights are downloaded from Hugging Face on the first model-backed run and cached locally. An internet connection is needed for that initial download, along with sufficient disk space and RAM.

## Run locally

### 1. Start the backend

From the repository root:

```bash
cd Task-5/backend
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Start the frontend

Open a second terminal:

```bash
cd Task-5/frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally [http://localhost:5173](http://localhost:5173)). The development frontend calls the backend at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Optional environment variables

- `HUMANCHECK_MODEL`: Hugging Face model ID (default shown above).
- `HUMANCHECK_ALLOW_HEURISTIC_FALLBACK`: set to `true` to allow heuristic fallback (default: true).
- `VITE_API_URL`: backend base URL for the frontend (local default: `http://127.0.0.1:8000`).

## Frontend deployment — GitHub Pages

The frontend is configured for GitHub Pages and a GitHub Actions workflow builds and deploys it.

1. Open the repository's [Pages settings](https://github.com/ranjiths112007/Codomax-Digital-Solutions-AI-ML-Internship-/settings/pages).
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open the [Actions tab](https://github.com/ranjiths112007/Codomax-Digital-Solutions-AI-ML-Internship-/actions) and check the **Deploy HumanCheck Frontend to GitHub Pages** workflow.
4. After a successful run, visit the [HumanCheck live frontend](https://ranjiths112007.github.io/Codomax-Digital-Solutions-AI-ML-Internship-/).

The workflow builds only `Task-5/frontend`; it does **not** deploy the Python backend. Therefore, the published site can display the frontend, but live analysis needs the FastAPI backend to be hosted separately and the frontend build variable `VITE_API_URL` set to that public backend URL. A browser cannot reach your own computer's `localhost` backend from the hosted site.

## API endpoints

- `GET /health` — API and model status.
- `POST /analyze` — JSON body: `{"text":"..."}`.
- `GET /docs` — interactive API documentation when running locally.

## Understanding the scores

The model returns class scores based on its training distribution. HumanCheck displays relative AI-like and human-like scores for comparison; these are **not calibrated authorship probabilities**. Very short text, non-English text, code, quotations, edited text, and domains unlike the model's training data can produce unreliable results. Sentence-level flags are explanatory pattern cues, not proof that a sentence was AI-written.

## Run tests

```bash
cd Task-5/backend
pip install -r requirements.txt
pytest -q
```

## Responsible use

- Treat results as a prompt for review, not a verdict.
- Preserve drafts, notes, version history, and source records when authorship matters.
- Avoid uploading private or sensitive content to a hosted service. This prototype is intended primarily for local use.
- Review the model card and licence for the chosen model before redistribution or production deployment.
