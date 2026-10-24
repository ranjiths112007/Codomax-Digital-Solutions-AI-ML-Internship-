"""Run a short, safe demo of the Expense Tracker and print its output."""

import tempfile
from pathlib import Path

from expense_tracker import (
    category_totals,
    load_expenses,
    save_expense,
    show_category_summary,
    show_expenses,
    total_spent,
)


def main():
    # Use a temporary file so the demo never changes your personal expenses.csv.
    with tempfile.TemporaryDirectory() as folder:
        data_file = Path(folder) / "demo_expenses.csv"

        print("=" * 42)
        print("EXPENSE TRACKER - SAMPLE RUN")
        print("=" * 42)

        save_expense("Food", 120, "Lunch", data_file, "2026-10-24")
        save_expense("Travel", 60, "Bus fare", data_file, "2026-10-24")
        save_expense("Food", 80, "Dinner", data_file, "2026-10-24")

        expenses = load_expenses(data_file)
        show_expenses(expenses)
        show_category_summary(expenses)

        print("\nDemo check:")
        print(f"Expenses recorded: {len(expenses)}")
        print(f"Total calculated: ₹{total_spent(expenses):.2f}")
        print(f"Category totals: {category_totals(expenses)}")
        print("\nDemo completed successfully.")


if __name__ == "__main__":
    main()
