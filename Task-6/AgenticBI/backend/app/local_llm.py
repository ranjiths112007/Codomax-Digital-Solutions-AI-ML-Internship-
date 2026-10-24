import os
import httpx

def narrate_findings(findings: list[dict]) -> str | None:
    base = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434').rstrip('/')
    model = os.getenv('OLLAMA_MODEL', 'qwen2.5:7b')
    evidence = '\n'.join(f"- {x.get('title')}: {x.get('detail')} Evidence: {x.get('evidence')}" for x in findings[:12])
    prompt = 'Write a concise business summary using only the validated evidence below. Do not invent numbers, causes, or facts. State uncertainty. Under 180 words.\n\n' + evidence
    try:
        response = httpx.post(base + '/api/generate', json={'model':model,'prompt':prompt,'stream':False}, timeout=45.0)
        response.raise_for_status()
        return response.json().get('response','').strip()[:4000] or None
    except (httpx.HTTPError, ValueError, KeyError):
        return None
