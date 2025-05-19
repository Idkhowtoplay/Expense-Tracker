import argparse
import json
import datetime
import os

data = "file.json"

def load_json():
    if not os.path.exists(data):
        return []
    with open (data, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        
def save_json(expense):
    with open(data, "w") as file:
        json.dump(expense, file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="add expense")
    add.add_argument("--description", help="description", required=True)
    add.add_argument("--amount", help="amount", required=True)

    update = subparsers.add_parser("update", help="update expense")
    update.add_argument("id", type=int, help="id")
    update.add_argument("--description",help="description", required=True)
    update.add_argument("--amount", help="amount", required=True)

    delete = subparsers.add_parser("delete", help="delete expense by id")
    delete.add_argument("--id", type=int, help="id the expense", required=True)

    summary = subparsers.add_parser("summary", help="see total expenses")
    summary.add_argument("--month", type=int, help="see total expenses by month", required=False)

    list = subparsers.add_parser("list", help="list all the expenses")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "list":
        list_all()
    elif args.command == "summary":
        if args.month:
            summary_by_month(args.month)
        else:
            summaryy()
    

def id_generator():
    expense = load_json()
    id = 1 + len(expense)
    return id

def date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def add_expense(name, number):
    expense = load_json()
    expens = {
        "ID": id_generator(),
        "Date": date(),
        "Description": name,
        "Amount": f"${number}"
    }
    expense.append(expens)
    save_json(expense)
    print(f"Expense added successfully (ID: {expens["ID"]})")

def delete_expense(id):
    expense = load_json()
    expense = [item for item in expense if item["ID"] != id]
    save_json(expense)
    print("Expense deleted successfully")

def update_expense(id, name, number):
    expense = load_json()
    for expens in expense:
        if expens["ID"] == id:
            expens["Description"] = name
            expens["Amount"] = f"${number}"
            save_json(expense)
            print("update successfully")

def list_all():
    expense = load_json()
    
    print(f" {"ID":<3} {"Date":<12} {"Description":<12} {"Amount":<6}")
    for row in expense:
        print(f" {row["ID"]:<3} {row["Date"]:<12} {row["Description"]:12} {row["Amount"]:6}")

def summaryy():
    expense = load_json()
    total = 0
    for e in expense:
        if e["Amount"]:
            total += int(e["Amount"].replace("$", ""))
    print(f"Total expenses: ${total}")

def summary_by_month(d):
    expense = load_json()
    total = 0
    month = ""
    for e in expense:
        date = datetime.datetime.strptime(e["Date"], "%Y-%m-%d")
        if date.month == d:
            total += int(e["Amount"].replace("$", ""))
            month += date.strftime("%B")
    print(f"Total expenses for {"".join(dict.fromkeys(month))}: ${total}")

main()
