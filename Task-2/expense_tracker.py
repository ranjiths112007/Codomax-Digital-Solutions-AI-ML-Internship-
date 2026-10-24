"""A small command-line expense tracker for everyday spending.

Expenses are saved in a CSV file, so they are still there next time you run
the program. This project uses only Python's standard library.
"""

import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDNAMES = ["date", "category", "amount", "note"]


def load_expenses(file_path=DATA_FILE):
    """Read saved expenses. Return an empty list if the file is not there yet."""
    if not file_path.exists():
        return []

    with file_path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_expense(category, amount, note="", file_path=DATA_FILE, expense_date=None):
    """Save one expense and return it as a dictionary."""
    if not category.strip():
        raise ValueError("Please enter a category.")
    if amount <= 0:
        raise ValueError("The amount must be greater than zero.")

    expense = {
        "date": expense_date or date.today().isoformat(),
        "category": category.strip().title(),
        "amount": f"{amount:.2f}",
        "note": note.strip(),
    }

    file_exists = file_path.exists()
    with file_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists or file_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(expense)

    return expense


def total_spent(expenses):
    """Add up the amount spent across all saved expenses."""
    return sum(float(expense["amount"]) for expense in expenses)


def category_totals(expenses):
    """Return the amount spent in each category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0.0) + float(expense["amount"])
    return totals


def show_expenses(expenses):
    """Print saved expenses in a simple, readable list."""
    if not expenses:
        print("\nNo expenses saved yet. Add your first one to get started.")
        return

    print("\nYour expenses")
    print("-" * 62)
    for item in expenses:
        note = f" — {item['note']}" if item.get("note") else ""
        print(
            f"{item['date']} | {item['category']:<14} | "
            f"₹{float(item['amount']):>8.2f}{note}"
        )
    print("-" * 62)
    print(f"Total spent: ₹{total_spent(expenses):.2f}")


def show_category_summary(expenses):
    """Show how much has been spent in each category."""
    totals = category_totals(expenses)
    if not totals:
        print("\nThere is nothing to summarise yet.")
        return

    print("\nSpending by category")
    print("-" * 30)
    for category, amount in sorted(totals.items()):
        print(f"{category:<18} ₹{amount:.2f}")
    print("-" * 30)
    print(f"{'All categories':<18} ₹{total_spent(expenses):.2f}")


def ask_for_amount():
    """Keep asking until the user enters a valid positive amount."""
    while True:
        try:
            amount = float(input("Amount (₹): ").strip())
            if amount <= 0:
                print("Enter an amount greater than zero.")
                continue
            return amount
        except ValueError:
            print("That doesn't look like a number. Try again.")


def main():
    print("\nWelcome to the Expense Tracker")
    print("A simple way to keep an eye on your spending.")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. View category summary")
        print("4. Exit")

        choice = input("Choose 1–4: ").strip()

        if choice == "1":
            category = input("Category (food, travel, bills, etc.): ").strip()
            amount = ask_for_amount()
            note = input("Short note (optional): ").strip()
            try:
                save_expense(category, amount, note)
                print("Expense saved. Nice and easy!")
            except ValueError as error:
                print(error)
        elif choice == "2":
            show_expenses(load_expenses())
        elif choice == "3":
            show_category_summary(load_expenses())
        elif choice == "4":
            print("Thanks for using the Expense Tracker. Take care!")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
