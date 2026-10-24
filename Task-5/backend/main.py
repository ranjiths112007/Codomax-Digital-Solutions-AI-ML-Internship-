"""HumanCheck local writing-pattern analysis API.

The detector is an assistive signal only. Text classification cannot establish authorship.
"""
from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from detector import analyze_text, get_detector_status

app = FastAPI(
    title="HumanCheck API",
    description="Local writing-pattern analysis. Results are estimates, not proof of authorship.",
    version="1.0.0",
)

allowed_origins = os.getenv(
    "HUMANCHECK_CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=30000)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "HumanCheck API",
        "message": "Local writing-pattern analysis, not an authorship verdict.",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", **get_detector_status()}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    text = request.text.strip()
    if len(text.split()) < 40:
        raise HTTPException(
            status_code=422,
            detail="Please provide at least 40 words for a more meaningful pattern analysis.",
        )
    try:
        return analyze_text(text)
    except Exception as exc:  # keep internal details out of the public response
        raise HTTPException(status_code=500, detail="Analysis failed. Check the backend logs.") from exc
