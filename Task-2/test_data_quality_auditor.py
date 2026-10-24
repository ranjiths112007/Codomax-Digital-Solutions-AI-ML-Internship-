"""Tests for the CSV data quality auditor."""

import tempfile
import unittest
from pathlib import Path

from data_quality_auditor import audit_csv


class DataQualityAuditorTests(unittest.TestCase):
    def test_detects_common_data_problems(self):
        content = (
            "customer_id,name,email,age\n"
            "C001,Ana,ana@example.com,24\n"
            "C002,Bob,bob.example.com,29\n"
            "C002,Bob,bob.example.com,29\n"
            "C003,,c@example.com,abc\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "customers.csv"
            path.write_text(content, encoding="utf-8")
            rows, issues = audit_csv(path)

        self.assertEqual(len(rows), 4)
        issue_names = {issue[1] for issue in issues}
        self.assertIn("Invalid email", issue_names)
        self.assertIn("Duplicate customer_id", issue_names)
        self.assertIn("Duplicate row", issue_names)
        self.assertIn("Missing name", issue_names)
        self.assertIn("Invalid age", issue_names)

    def test_rejects_missing_required_columns(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text("name,email\nAna,ana@example.com\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit_csv(path)


if __name__ == "__main__":
    unittest.main()
