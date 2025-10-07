
import csv
import json
import os
from datetime import datetime, date
from statistics import mean

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budgets.json"
CATEGORIES = ["Food", "Rent", "Transport", "Utilities", "Health",
              "Education", "Entertainment", "Other"]

CSV_FIELDS = ["date", "amount", "category", "note"]  


def ensure_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)  # no budgets yet


def load_budgets():
    with open(BUDGET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_budgets(budgets):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2)


def read_expenses():
    rows = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def append_expense(row):
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(row)


def add_expense():
    try:
        raw_date = input("Date (YYYY-MM-DD, blank=today): ").strip()
        if raw_date == "":
            d = date.today()
        else:
            d = datetime.strptime(raw_date, "%Y-%m-%d").date()

        amount = float(input("Amount (e.g., 12.50): ").strip())

        print("Categories:", ", ".join(CATEGORIES))
        cat = input("Category: ").strip() or "Other"
        if cat not in CATEGORIES:
            print("Unknown category. Using 'Other'.")
            cat = "Other"

        note = input("Note (optional): ").strip()

        append_expense({
            "date": d.isoformat(),
            "amount": f"{amount:.2f}",
            "category": cat,
            "note": note
        })
        print("Expense added.")
    except Exception as e:
        print("Failed to add expense:", e)


def set_budget():
    budgets = load_budgets()
    print("Categories:", ", ".join(CATEGORIES))
    cat = input("Category to set budget for: ").strip()
    if cat not in CATEGORIES:
        print("Unknown category.")
        return
    try:
        amt = float(input("Monthly budget amount: ").strip())
        budgets[cat] = round(amt, 2)
        save_budgets(budgets)
        print(f"Budget set for {cat}: {amt:.2f}")
    except Exception as e:
        print("Invalid amount:", e)


def show_budgets():
    budgets = load_budgets()
    if not budgets:
        print("(No budgets set.)")
        return
    print("\n== Budgets ==")
    for k, v in budgets.items():
        print(f"{k:15}  ${v:,.2f}")


def monthly_report():
    rows = read_expenses()
    if not rows:
        print("(No expenses yet.)")
        return

    ym = input("Month to report (YYYY-MM), blank=this month: ").strip()
    if ym == "":
        today = date.today()
        ym = f"{today.year:04d}-{today.month:02d}"

    month_rows = [r for r in rows if r["date"].startswith(ym + "-")]
    if not month_rows:
        print(f"(No expenses in {ym}.)")
        return

    budgets = load_budgets()
    total = 0.0
    by_cat = {}
    amounts = []

    for r in month_rows:
        amt = float(r["amount"])
        total += amt
        amounts.append(amt)
        by_cat[r["category"]] = by_cat.get(r["category"], 0.0) + amt

    print(f"\n== Monthly report for {ym} ==")
    print(f"Total spent: ${total:,.2f}")
    print(f"Transactions: {len(month_rows)}")
    print(f"Average txn: ${mean(amounts):.2f}")

    print("\n-- By Category --")
    for cat, cat_total in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        budget = budgets.get(cat)
        line = f"{cat:15} ${cat_total:,.2f}"
        if budget is not None:
            if cat_total > budget:
                line += f"  (⚠ over by ${cat_total - budget:,.2f}; budget ${budget:,.2f})"
            else:
                line += f"  (✓ under budget ${budget:,.2f})"
        print(line)

    top5 = sorted(month_rows, key=lambda r: float(r["amount"]), reverse=True)[:5]
    print("\n-- Top 5 expenses --")
    for r in top5:
        print(f"{r['date']}  ${float(r['amount']):7.2f}  {r['category']:12}  {r['note']}")


def category_report():
    rows = read_expenses()
    if not rows:
        print("(No expenses yet.)")
        return
    cat = input("Category (blank to list all totals): ").strip()

    if cat == "":

        totals = {}
        for r in rows:
            totals[r["category"]] = totals.get(r["category"], 0.0) + float(r["amount"])
        print("\n== All-time totals by category ==")
        for k, v in sorted(totals.items(), key=lambda kv: -kv[1]):
            print(f"{k:15} ${v:,.2f}")
        return

    filt = [r for r in rows if r["category"] == cat]
    if not filt:
        print(f"(No expenses in category '{cat}'.)")
        return

    per_month = {}
    for r in filt:
        ym = r["date"][:7]
        per_month[ym] = per_month.get(ym, 0.0) + float(r["amount"])

    print(f"\n== '{cat}' spend per month ==")
    for ym, total in sorted(per_month.items()):
        print(f"{ym}: ${total:,.2f}")


def list_recent(n=20):
    rows = read_expenses()
    print(f"\n== Last {n} expenses ==")
    for r in rows[-n:]:
        print(f"{r['date']}  ${float(r['amount']):7.2f}  {r['category']:12}  {r['note']}")


def menu():
    ensure_files()
    actions = {
        "1": add_expense,
        "2": list_recent,
        "3": monthly_report,
        "4": category_report,
        "5": set_budget,
        "6": show_budgets,
        "0": lambda: (_ for _ in ()).throw(SystemExit),
    }
    while True:
        print("\n=== Expense Tracker ===")
        print("1) Add expense")
        print("2) Show recent expenses")
        print("3) Monthly report (with budget alerts)")
        print("4) Category report")
        print("5) Set monthly budget (by category)")
        print("6) Show budgets")
        print("0) Exit")
        choice = input("> ").strip()
        action = actions.get(choice)
        try:
            if action:
                action()
            else:
                print("Invalid choice.")
        except SystemExit:
            print("Bye!")
            break
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()
