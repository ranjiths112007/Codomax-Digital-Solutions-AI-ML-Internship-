"""A few checks to make sure the expense tracker behaves as expected."""

import tempfile
import unittest
from pathlib import Path

from expense_tracker import category_totals, load_expenses, save_expense, total_spent


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "test_expenses.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_expense(self):
        save_expense("food", 120.5, "Lunch", self.data_file, "2026-10-24")
        expenses = load_expenses(self.data_file)

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertEqual(float(expenses[0]["amount"]), 120.5)
        self.assertEqual(expenses[0]["note"], "Lunch")

    def test_total_spent(self):
        expenses = [
            {"amount": "50.00"},
            {"amount": "25.50"},
        ]
        self.assertEqual(total_spent(expenses), 75.5)

    def test_category_totals(self):
        expenses = [
            {"category": "Food", "amount": "100.00"},
            {"category": "Food", "amount": "50.00"},
            {"category": "Travel", "amount": "40.00"},
        ]
        self.assertEqual(category_totals(expenses), {"Food": 150.0, "Travel": 40.0})

    def test_reject_empty_category(self):
        with self.assertRaises(ValueError):
            save_expense("  ", 10, file_path=self.data_file)

    def test_reject_non_positive_amount(self):
        with self.assertRaises(ValueError):
            save_expense("Food", 0, file_path=self.data_file)


if __name__ == "__main__":
    unittest.main()
