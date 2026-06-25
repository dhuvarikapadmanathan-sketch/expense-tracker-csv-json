"""
Task 3: Expense Tracker (CSV/JSON)
------------------------------------
A command-line expense tracker that lets you add, view, filter, and
summarize expenses. Data is persisted to a CSV file, and a JSON export
option is also provided.

Usage:
    python expense_tracker.py
"""

import csv
import json
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
FIELDNAMES = ["date", "category", "description", "amount"]


def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def add_expense():
    date_str = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    category = input("Category (e.g. Food, Travel, Bills): ").strip() or "Uncategorized"
    description = input("Description: ").strip()

    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount.")
        return

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "date": date_str,
            "category": category,
            "description": description,
            "amount": amount,
        })

    print("Expense added successfully!")


def read_expenses():
    init_file()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def view_expenses():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'Date':<12}{'Category':<15}{'Description':<25}{'Amount':>10}")
    print("-" * 62)
    total = 0
    for e in expenses:
        amount = float(e["amount"])
        total += amount
        print(f"{e['date']:<12}{e['category']:<15}{e['description'][:24]:<25}{amount:>10.2f}")
    print("-" * 62)
    print(f"{'TOTAL':<52}{total:>10.2f}")


def filter_by_category():
    expenses = read_expenses()
    category = input("Enter category to filter: ").strip().lower()
    filtered = [e for e in expenses if e["category"].lower() == category]

    if not filtered:
        print("No expenses found for that category.")
        return

    total = sum(float(e["amount"]) for e in filtered)
    print(f"\n{'Date':<12}{'Description':<25}{'Amount':>10}")
    for e in filtered:
        print(f"{e['date']:<12}{e['description'][:24]:<25}{float(e['amount']):>10.2f}")
    print(f"\nTotal for '{category}': {total:.2f}")


def monthly_summary():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}
    for e in expenses:
        month = e["date"][:7]  # YYYY-MM
        summary[month] = summary.get(month, 0) + float(e["amount"])

    print("\nMonthly Summary:")
    for month, total in sorted(summary.items()):
        print(f"  {month}: {total:.2f}")


def export_to_json():
    expenses = read_expenses()
    json_file = "expenses_export.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)
    print(f"Exported to {json_file}")


def main():
    init_file()
    menu = """
===== EXPENSE TRACKER =====
1. Add Expense
2. View All Expenses
3. Filter by Category
4. Monthly Summary
5. Export to JSON
6. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_by_category()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            export_to_json()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
