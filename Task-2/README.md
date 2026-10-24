# Task 2 — Python Mini Project: Expense Tracker

**Module:** 02  
**Schedule:** Day 5–Day 8  
**Level:** Beginner

## What this project does

This is a small command-line app for keeping track of everyday expenses. You can add a purchase, see the expenses you have saved, and check how much you have spent in each category.

It saves entries in a CSV file, so your records remain available when you close and reopen the program. It uses Python's built-in tools, so you do not need to install extra packages.

## Features

- Add an expense with a category, amount, and optional note.
- Save the date and details to `expenses.csv`.
- View all saved expenses and the total amount spent.
- See spending grouped by category.
- Get a helpful message if the amount or menu choice is invalid.
- Run a few unit tests to check the main functions.

## Files

- `expense_tracker.py` — the app and its menu.
- `test_expense_tracker.py` — tests for saving, loading, totals, and input validation.
- `expenses.csv` — created automatically when you save your first expense.

## How to run it

Make sure Python 3 is installed. Open a terminal in this folder and run:

```bash
python expense_tracker.py
```

Follow the menu and enter the details when asked. You can use categories such as Food, Travel, Shopping, or Bills.

## Run the tests

From inside the `Task-2` folder, run:

```bash
python -m unittest -v
```

The tests use a temporary CSV file, so they will not change your own expense records.

## Example

```text
Welcome to the Expense Tracker
A simple way to keep an eye on your spending.

What would you like to do?
1. Add an expense
2. View all expenses
3. View category summary
4. Exit
Choose 1–4: 1
Category (food, travel, bills, etc.): food
Amount (₹): 120
Short note (optional): Lunch
Expense saved. Nice and easy!
```

## What I learned

This project gave me practice with Python functions, loops, conditions, exception handling, file paths, CSV files, and unit testing. It also helped me turn separate Python concepts into one useful little program.

---

**Task 2:** Python Mini Project — completed as part of the Codomax Digital Solutions AI & ML Internship learning tasks.
