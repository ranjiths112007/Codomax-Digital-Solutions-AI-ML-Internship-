"""Local model inference and transparent heuristic fallback for HumanCheck."""
from __future__ import annotations

import math
import os
import re
import statistics
from collections import Counter
from functools import lru_cache
from typing import Any

MODEL_ID = os.getenv("HUMANCHECK_MODEL", "openai-community/roberta-base-openai-detector")
ALLOW_FALLBACK = os.getenv("HUMANCHECK_ALLOW_HEURISTIC_FALLBACK", "true").lower() in {"1", "true", "yes"}

_WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in _SENTENCE_RE.split(text.strip()) if part.strip()]


def text_metrics(text: str) -> dict[str, Any]:
    words = _WORD_RE.findall(text)
    sentences = split_sentences(text)
    lengths = [len(_WORD_RE.findall(sentence)) for sentence in sentences]
    unique_ratio = len({word.lower() for word in words}) / max(len(words), 1)
    mean_length = statistics.mean(lengths) if lengths else 0.0
    std_length = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    repeated_words = Counter(word.lower() for word in words if len(word) > 3)
    repetition = sum(count - 1 for count in repeated_words.values() if count > 1) / max(len(words), 1)
    transition_phrases = [
        "in conclusion", "furthermore", "moreover", "in addition", "it is important to note",
        "on the other hand", "overall", "delve into", "in today's world", "plays a crucial role",
        "in summary", "firstly", "secondly", "lastly",
    ]
    lower = text.lower()
    transition_hits = sum(lower.count(phrase) for phrase in transition_phrases)
    punctuation_variety = len(set(re.findall(r"[,;:!?—-]", text)))
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "character_count": len(text),
        "average_sentence_length": round(mean_length, 1),
        "sentence_length_variation": round(std_length, 1),
        "vocabulary_diversity": round(unique_ratio * 100, 1),
        "repeated_word_ratio": round(repetition * 100, 1),
        "transition_phrase_count": transition_hits,
        "punctuation_variety": punctuation_variety,
    }


def _heuristic_score(text: str, metrics: dict[str, Any]) -> tuple[float, list[str]]:
    """A weak, explainable style heuristic; deliberately not called a trained AI detector."""
    score = 50.0
    cues: list[str] = []
    if metrics["sentence_count"] >= 4:
        variation = metrics["sentence_length_variation"]
        if variation < 4:
            score += 10
            cues.append("Sentence lengths are relatively uniform.")
        elif variation > 10:
            score -= 5
            cues.append("Sentence lengths vary noticeably.")
    if metrics["transition_phrase_count"] >= 2:
        score += min(12, metrics["transition_phrase_count"] * 3)
        cues.append("Several formal transition phrases appear.")
    if metrics["repeated_word_ratio"] > 12:
        score += 6
        cues.append("Some longer words repeat frequently.")
    if metrics["vocabulary_diversity"] > 75:
        score -= 4
        cues.append("The text uses a broad range of vocabulary.")
    elif metrics["vocabulary_diversity"] < 38 and metrics["word_count"] > 100:
        score += 4
        cues.append("Vocabulary is relatively repetitive.")
    if metrics["punctuation_variety"] >= 4:
        score -= 3
        cues.append("Punctuation varies across the text.")
    if not cues:
        cues.append("There are no strong signals in the simple style checks.")
    return max(5.0, min(95.0, score)), cues


@lru_cache(maxsize=1)
def _load_pipeline():
    from transformers import pipeline
    return pipeline("text-classification", model=MODEL_ID, tokenizer=MODEL_ID, device=-1)


def get_detector_status() -> dict[str, Any]:
    return {
        "model_id": MODEL_ID,
        "model_load": "lazy (loads on first analysis)",
        "fallback_enabled": ALLOW_FALLBACK,
        "privacy": "text is processed by this local backend and is not stored by the application",
    }


def _model_ai_score(text: str) -> tuple[float, list[str]]:
    classifier = _load_pipeline()
    # Keep each chunk under the model token limit. The output is averaged across chunks.
    chunks = split_sentences(text)
    chunks = chunks or [text]
    grouped: list[str] = []
    current = ""
    for sentence in chunks:
        if len((current + " " + sentence).split()) > 180 and current:
            grouped.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        grouped.append(current)

    scores: list[float] = []
    for chunk in grouped[:20]:
        result = classifier(chunk[:4000], truncation=True, max_length=512)[0]
        label = str(result.get("label", "")).lower()
        confidence = float(result.get("score", 0.5))
        if any(token in label for token in ("fake", "ai", "gpt", "generated")):
            ai_score = confidence
        elif any(token in label for token in ("real", "human", "original")):
            ai_score = 1.0 - confidence
        else:
            # Most detector checkpoints map index 0 to Fake and index 1 to Real.
            ai_score = confidence if label in {"label_0", "0"} else 1.0 - confidence
        scores.append(ai_score)
    return sum(scores) / len(scores), [
        "Scores come from a locally running text-classification model.",
        "Model scores are not calibrated probabilities of authorship.",
    ]


def analyze_text(text: str) -> dict[str, Any]:
    metrics = text_metrics(text)
    model_error: str | None = None
    try:
        ai_fraction, cues = _model_ai_score(text)
        method = "local-ml-model"
        ai_score = round(max(0.0, min(1.0, ai_fraction)) * 100, 1)
        human_score = round(100.0 - ai_score, 1)
    except Exception as exc:
        if not ALLOW_FALLBACK:
            raise
        model_error = type(exc).__name__
        ai_score, cues = _heuristic_score(text, metrics)
        human_score = round(100.0 - ai_score, 1)
        method = "heuristic-fallback"
        cues.insert(0, "The ML model was unavailable; this is a simple writing-pattern heuristic, not a trained detector.")

    sentences = split_sentences(text)
    sentence_analysis = []
    for index, sentence in enumerate(sentences[:80]):
        sentence_metrics = text_metrics(sentence)
        local_score, local_cues = _heuristic_score(sentence, sentence_metrics)
        sentence_analysis.append({
            "index": index,
            "text": sentence,
            "pattern_signal": "more AI-like patterns" if local_score >= 60 else "more human-like patterns" if local_score <= 40 else "mixed / inconclusive patterns",
            "heuristic_score": round(local_score, 1),
            "cues": local_cues[:2],
        })

    if ai_score >= 65:
        summary = "The text has patterns the selected detector associates more strongly with AI-generated examples."
    elif ai_score <= 35:
        summary = "The text has patterns the selected detector associates more strongly with human-written examples."
    else:
        summary = "The result is mixed. The available writing patterns do not strongly favour either category."

    return {
        "ai_like_score": ai_score,
        "human_like_score": human_score,
        "summary": summary,
        "method": method,
        "model_id": MODEL_ID if method == "local-ml-model" else None,
        "metrics": metrics,
        "signals": cues,
        "sentences": sentence_analysis,
        "limitations": [
            "This is an estimate of text patterns, not proof of who wrote the text.",
            "The percentages are not calibrated probabilities and should not be treated as certainty.",
            "Short text, edited text, non-English text, quotations, and unfamiliar writing styles can reduce reliability.",
            "Do not use this result as the sole basis for academic, employment, or disciplinary decisions.",
        ],
        "model_load_error_type": model_error,
    }
