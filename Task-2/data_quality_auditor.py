"""Find common data problems in a CSV file before analysis."""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_COLUMNS = {"customer_id", "name", "email", "age"}
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def audit_csv(file_path):
    with Path(file_path).open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = set(reader.fieldnames or [])

        if not headers:
            raise ValueError("The CSV file is empty or has no header row.")

        missing_columns = sorted(REQUIRED_COLUMNS - headers)
        if missing_columns:
            raise ValueError("Missing required columns: " + ", ".join(missing_columns))

        rows = list(reader)

    issues = []
    seen_rows = set()
    seen_ids = set()

    for line_number, row in enumerate(rows, start=2):
        normalized = tuple((value or "").strip() for value in row.values())

        if normalized in seen_rows:
            issues.append((line_number, "Duplicate row", "This row repeats an earlier record."))
        seen_rows.add(normalized)

        customer_id = (row.get("customer_id") or "").strip()
        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip()
        age = (row.get("age") or "").strip()

        if not customer_id:
            issues.append((line_number, "Missing customer_id", "Customer ID is blank."))
        elif customer_id in seen_ids:
            issues.append((line_number, "Duplicate customer_id", f"ID '{customer_id}' already exists."))
        seen_ids.add(customer_id)

        if not name:
            issues.append((line_number, "Missing name", "Name is blank."))

        if not email:
            issues.append((line_number, "Missing email", "Email is blank."))
        elif not EMAIL_PATTERN.match(email):
            issues.append((line_number, "Invalid email", f"'{email}' is not a valid email format."))

        if not age:
            issues.append((line_number, "Missing age", "Age is blank."))
        else:
            try:
                age_value = int(age)
                if not 0 <= age_value <= 120:
                    issues.append((line_number, "Age out of range", f"Age '{age}' must be between 0 and 120."))
            except ValueError:
                issues.append((line_number, "Invalid age", f"'{age}' is not a whole number."))

    return rows, issues


def main():
    file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("sample_customers.csv")

    try:
        rows, issues = audit_csv(file_path)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Audit failed: {error}")
        raise SystemExit(1)

    print("\nCSV DATA QUALITY AUDIT")
    print("=" * 52)
    print(f"File: {file_path.name}")
    print(f"Rows checked: {len(rows)}")
    print(f"Issues found: {len(issues)}")

    if issues:
        print("\nISSUES")
        print("-" * 52)
        for line_number, issue, details in issues:
            print(f"Row {line_number}: {issue} — {details}")
    else:
        print("\nNo data quality issues found.")

    print("\nAudit complete.")


if __name__ == "__main__":
    main()
