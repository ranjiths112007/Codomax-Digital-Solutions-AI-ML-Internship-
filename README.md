# Codomax Digital Solutions — AI & ML Internship
## AI & ML Internship Tasks

This repository contains internship projects for Modules 01–04, including Python fundamentals, data quality auditing, data analysis and visualization, and machine learning fundamentals.

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
├── Task-1/
│   ├── README.md
│   ├── ai_ml_dl_and_real_world_applications.md
│   ├── python_basics.py
│   ├── control_flow_and_lists.py
│   ├── beginner_programs.py
│   └── test_beginner_programs.py
└── Task-2/
    ├── README.md
    ├── expense_tracker.py
    └── test_expense_tracker.py
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

### 3. Run the programs

```bash
python Task-1/python_basics.py
python Task-1/control_flow_and_lists.py
python Task-1/beginner_programs.py
```

The programs use Python's standard library, so no external packages are required.

### 4. Run the tests

From the repository root:

```bash
python -m unittest discover -s Task-1 -p "test_*.py"
```

## Task 2 — CSV Data Quality Auditor

Checks a dataset for missing values, duplicate records and IDs, invalid email formats, and out-of-range ages. Run it with `python Task-2/data_quality_auditor.py`. The sample data includes deliberate issues so the report is visible. See [`Task-2/README.md`](Task-2/README.md) for the short instructions.

## Task 3 — Data Analysis & Visualization

Uses Pandas and NumPy to explore and clean sample sales data, calculate revenue summaries, and create bar, line, and pie charts with Matplotlib. Open `Task-3/Module_03_Data_Analysis_Visualization.ipynb` in Google Colab and run all cells.

## Task 4 — Machine Learning Fundamentals

Trains and evaluates a Random Forest classifier on the Iris dataset using Scikit-learn. Includes a train/test split, accuracy, classification report, confusion matrix, and a new-flower prediction. Open `Task-4/Module_04_Machine_Learning_Fundamentals.ipynb` in Google Colab and run all cells.

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
**Note:** This repository documents learning exercises for Task 1. Make sure you understand and can explain the code before submitting it.
