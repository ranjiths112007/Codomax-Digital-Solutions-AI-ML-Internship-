# Task 2 — CSV Data Quality Auditor

A small Python tool that checks a CSV dataset for common problems before analysis: missing values, duplicate records or IDs, invalid email formats, and ages outside the valid range.

**Run it**
```bash
python Task-2/data_quality_auditor.py
```

Check another CSV:
```bash
python Task-2/data_quality_auditor.py path/to/your_file.csv
```

Run tests:
```bash
python -m unittest discover -s Task-2 -p "test_*.py" -v
```

The included sample intentionally contains data issues so the report has visible results. No extra packages are needed.
