from io import BytesIO
from typing import Any
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

MAX_ROWS = 50_000
MAX_COLUMNS = 100

def analyze_csv(raw: bytes, filename: str = 'upload.csv') -> dict[str, Any]:
    try:
        df = pd.read_csv(BytesIO(raw), nrows=MAX_ROWS + 1)
    except Exception as exc:
        raise ValueError(f'Could not read CSV: {exc}') from exc
    if df.empty:
        raise ValueError('The CSV has no data rows.')
    if len(df) > MAX_ROWS:
        raise ValueError(f'CSV exceeds the {MAX_ROWS:,}-row limit.')
    if len(df.columns) > MAX_COLUMNS:
        raise ValueError(f'CSV exceeds the {MAX_COLUMNS}-column limit.')
    missing = df.isna().sum()
    duplicate_rows = int(df.duplicated().sum())
    work = df.copy()
    for col in work.select_dtypes(include='object').columns:
        work[col] = work[col].map(lambda x: x.strip() if isinstance(x, str) else x).replace('', np.nan)
    numeric_cols = work.select_dtypes(include='number').columns.tolist()
    numeric_summary = {}
    for col in numeric_cols[:20]:
        s = pd.to_numeric(work[col], errors='coerce').dropna()
        if not s.empty:
            numeric_summary[str(col)] = {'count': int(s.count()), 'mean': round(float(s.mean()), 4), 'median': round(float(s.median()), 4), 'min': round(float(s.min()), 4), 'max': round(float(s.max()), 4), 'sum': round(float(s.sum()), 4)}
    top_categories = {}
    for col in [c for c in work.columns if c not in numeric_cols][:10]:
        counts = work[col].fillna('(missing)').astype(str).value_counts().head(5)
        top_categories[str(col)] = [{'value': str(k)[:120], 'count': int(v)} for k, v in counts.items()]
    anomalies = []
    if len(numeric_cols) >= 2 and len(work) >= 20:
        features = work[numeric_cols[:20]].replace([np.inf, -np.inf], np.nan)
        features = features.fillna(features.median()).fillna(0)
        if features.nunique().gt(1).sum() >= 2:
            model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
            labels = model.fit_predict(features)
            scores = model.decision_function(features)
            anomalies = [{'row_number': int(i + 2), 'anomaly_score': round(float(scores[i]), 5)} for i in np.flatnonzero(labels == -1)[:10]]
    findings = []
    missing_total = int(missing.sum())
    if missing_total:
        findings.append({'title':'Missing values detected','detail':f'{missing_total:,} cells are missing across {int((missing > 0).sum())} columns.','evidence':'Computed from pandas missing-value counts.'})
    if duplicate_rows:
        findings.append({'title':'Duplicate rows detected','detail':f'{duplicate_rows:,} rows are exact duplicates.','evidence':'Computed from DataFrame.duplicated().'})
    if numeric_summary:
        col, stat = max(numeric_summary.items(), key=lambda item: abs(item[1]['sum']))
        findings.append({'title':f'Largest absolute numeric total: {col}','detail':f'Sum = {stat["sum"]}; mean = {stat["mean"]}.','evidence':f'Computed from numeric column {col}.'})
    if anomalies:
        findings.append({'title':'Potential unusual records','detail':f'Isolation Forest flagged {len(anomalies)} example rows (up to 10 shown).','evidence':'Unsupervised anomaly detection; review before action.'})
    if not findings:
        findings.append({'title':'Initial profile complete','detail':'No missing values, exact duplicates, or anomaly examples were identified by the configured checks.','evidence':'Automated checks only; this does not guarantee data quality.'})
    preview = work.head(8).astype(object).where(pd.notna(work.head(8)), None).to_dict(orient='records')
    return {'filename':filename,'shape':{'rows':int(len(df)),'columns':int(len(df.columns))},'columns':[{'name':str(c),'dtype':str(df[c].dtype)} for c in df.columns],'data_quality':{'missing_cells':missing_total,'missing_by_column':{str(k):int(v) for k,v in missing.items() if v},'duplicate_rows':duplicate_rows,'blank_cells_after_trim':int(work.isna().sum().sum())},'numeric_summary':numeric_summary,'top_categories':top_categories,'anomalies':anomalies,'findings':findings,'preview':preview,'notes':['Statistics are calculated locally.','Anomaly flags are investigation leads, not proof of fraud or errors.','The uploaded file is not modified.']}
