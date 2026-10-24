# Codomax Digital Solutions — AI & ML Internship

## AI & ML Internship Tasks

This repository contains internship projects for Modules 01–05, covering Python fundamentals, data quality auditing, data analysis and visualization, machine learning fundamentals, and a local-first writing pattern analyzer.

**HumanCheck — Task 5 live frontend:** [Open the deployed site](https://ranjiths112007.github.io/Codomax-Digital-Solutions-AI-ML-Internship-/)

## Task 1 — Introduction to AI & Python

### Objectives covered
1. Learn the basics of Artificial Intelligence and Machine Learning.
2. Understand the difference between AI, ML, and Deep Learning.
3. Explore real-world AI applications.
4. Install Python and practise variables, loops, functions, and lists.
5. Write beginner-friendly Python programs.

### Task contents

- **AI, ML, and Deep Learning notes:** Definitions, differences, relationships, real-world examples, key terms, and review questions.
- **Python basics:** Variables, data types, operators, type conversion, lists, and functions.
- **Control flow and collections:** Conditions, `for` and `while` loops, list operations, list comprehensions, and simple calculations.
- **Beginner Python programs:** Even/odd checker, multiplication table, factorial, palindrome checker, calculator, and list statistics.
- **Tests:** Basic unit tests for the beginner practice programs.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── deploy-humancheck.yml
├── Task-1/
│   ├── README.md
│   ├── ai_ml_dl_and_real_world_applications.md
│   ├── python_basics.py
│   ├── control_flow_and_lists.py
│   ├── beginner_programs.py
│   └── test_beginner_programs.py
├── Task-2/
│   ├── README.md
│   ├── expense_tracker.py
│   └── test_expense_tracker.py
├── Task-3/
│   └── Module_03_Data_Analysis_Visualization.ipynb
├── Task-4/
│   └── Module_04_Machine_Learning_Fundamentals.ipynb
└── Task-5/
    ├── README.md
    ├── backend/
    └── frontend/
```

## Setup and run

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). On Windows, enable **Add Python to PATH** during installation.

Check the installation:

```bash
python --version
```

### 2. Clone this repository

```bash
git clone https://github.com/ranjiths112007/Codomax-Digital-Solutions-AI-ML-Internship-.git
cd Codomax-Digital-Solutions-AI-ML-Internship-
```

### 3. Run Task 1 programs

```bash
python Task-1/python_basics.py
python Task-1/control_flow_and_lists.py
python Task-1/beginner_programs.py
```

The Task 1 programs use Python's standard library, so no external packages are required.

### 4. Run Task 1 tests

From the repository root:

```bash
python -m unittest discover -s Task-1 -p "test_*.py"
```

## Task 2 — CSV Data Quality Auditor

Checks a dataset for missing values, duplicate records and IDs, invalid email formats, and out-of-range ages. Run it with `python Task-2/data_quality_auditor.py`. The sample data includes deliberate issues so the report is visible. See [Task 2 README](Task-2/README.md) for instructions.

## Task 3 — Data Analysis & Visualization

Uses Pandas and NumPy to explore and clean sample sales data, calculate revenue summaries, and create bar, line, and pie charts with Matplotlib. Open `Task-3/Module_03_Data_Analysis_Visualization.ipynb` in Google Colab and run all cells.

## Task 4 — Machine Learning Fundamentals

Trains and evaluates a Random Forest classifier on the Iris dataset using Scikit-learn. Includes a train/test split, accuracy, classification report, confusion matrix, and a new-flower prediction. Open `Task-4/Module_04_Machine_Learning_Fundamentals.ipynb` in Google Colab and run all cells.

## Task 5 — HumanCheck: Local Writing Pattern Analyzer

**[Launch the HumanCheck frontend](https://ranjiths112007.github.io/Codomax-Digital-Solutions-AI-ML-Internship-/)** · **[Read Task 5 documentation](Task-5/README.md)** · **[View Task 5 source](Task-5/)**

HumanCheck is a full-stack prototype with a React + Vite frontend and a FastAPI backend. It estimates AI-like and human-like writing patterns, shows sentence-level cues, and explains its results.

- **Frontend:** `Task-5/frontend/` — responsive React application, deployed to GitHub Pages.
- **Backend:** `Task-5/backend/` — FastAPI API, local model inference, writing-pattern metrics, fallback analysis, and tests.
- **Model:** Hugging Face `openai-community/roberta-base-openai-detector`, downloaded and cached locally on first model-backed run.
- **API key:** No paid inference API key is required.
- **Deployment:** GitHub Actions builds and deploys the frontend. The backend is not hosted by GitHub Pages and must be deployed separately for hosted text analysis to work. See the Task 5 README for setup and deployment details.

**Responsible use:** The displayed scores are not calibrated probabilities and cannot prove authorship. Human writing can be misclassified, and AI-generated writing can appear human. Do not use the tool as the sole basis for academic, employment, or disciplinary decisions.

## Key concepts

- **Artificial Intelligence (AI):** The broad field of building systems that perform tasks associated with human intelligence.
- **Machine Learning (ML):** A subset of AI where models learn patterns from data.
- **Deep Learning (DL):** A subset of ML that uses neural networks with multiple layers.

In general, **Deep Learning ⊂ Machine Learning ⊂ Artificial Intelligence**. Not every AI system uses machine learning, and not every ML model uses deep learning.

## Real-world applications

- Healthcare: image analysis support and clinical-data pattern detection.
- Finance: fraud detection and risk modelling.
- Transportation: route prediction and driver-assistance systems.
- Retail: recommendations and demand forecasting.
- Agriculture: crop monitoring and possible plant-disease detection.
- Language: translation, speech recognition, summarisation, and question answering.

AI systems can make mistakes. Their outputs need appropriate testing and human oversight, with attention to privacy, fairness, and safety.

## Task 1 checklist

- [ ] Review the AI, ML, and Deep Learning notes.
- [ ] Install Python and verify the installation.
- [ ] Run each Python example.
- [ ] Modify the examples and understand the output.
- [ ] Run the unit tests.
- [ ] Review and commit the completed work.

---

**Note:** This repository documents learning exercises and internship tasks. Make sure you understand and can explain the code before submitting it.
