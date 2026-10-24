import os
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .analysis import analyze_csv
from .local_llm import narrate_findings
from .report import build_presentation

MAX_UPLOAD_BYTES = 15 * 1024 * 1024
app = FastAPI(title='AgenticBI API', version='0.1.0', description='Local CSV analysis and PowerPoint generation')
app.add_middleware(CORSMiddleware, allow_origins=os.getenv('CORS_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(','), allow_credentials=False, allow_methods=['GET','POST'], allow_headers=['*'])

async def _read_csv(file: UploadFile) -> bytes:
    if not file.filename or not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Please upload a .csv file.')
    raw = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES: raise HTTPException(status_code=413, detail='Upload exceeds 15 MB.')
    if not raw: raise HTTPException(status_code=400, detail='The uploaded file is empty.')
    return raw

@app.get('/api/health')
def health(): return {'status':'ok','project':'AgenticBI','local_llm_optional':True}

@app.post('/api/analyze')
async def analyze(file: UploadFile = File(...)):
    raw = await _read_csv(file)
    try: result = analyze_csv(raw, file.filename or 'upload.csv')
    except ValueError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    narrative = narrate_findings(result['findings']); result['narrative'] = narrative
    result['narrative_source'] = 'local_ollama' if narrative else 'deterministic_findings'
    return result

@app.post('/api/report')
async def report(file: UploadFile = File(...)):
    raw = await _read_csv(file)
    try: result = analyze_csv(raw, file.filename or 'upload.csv'); pptx = build_presentation(result)
    except ValueError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    safe = (file.filename or 'analysis').rsplit('.',1)[0][:80]
    return Response(content=pptx, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', headers={'Content-Disposition':f'attachment; filename="{safe}_agenticbi_report.pptx"'})
