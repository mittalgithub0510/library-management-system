import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = "bank_data.json"

# ---------- Data Models ----------
class Customer:
    def _init_(self, name, customer_id):
        self.name = name
        self.customer_id = customer_id
        self.accounts = []

    def to_dict(self):
        return {
            "name": self.name,
            "customer_id": self.customer_id,
            "accounts": self.accounts
        }

class BankAccount:
    def _init_(self, acc_number, customer_id, acc_type, balance=0.0):
        self.acc_number = acc_number
        self.customer_id = customer_id
        self.acc_type = acc_type
        self.balance = balance
        self.overdraft_limit = 500 if acc_type == "Checking" else 0
        self.transactions = []

    def to_dict(self):
        return {
            "acc_number": self.acc_number,
            "customer_id": self.customer_id,
            "acc_type": self.acc_type,
            "balance": self.balance,
            "overdraft_limit": self.overdraft_limit,
            "transactions": self.transactions
        }

# ---------- Persistence ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"customers": {}, "accounts": {}}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

data = load_data()

# ---------- Business Logic ----------
def add_customer():
    name = simpledialog.askstring("Add Customer", "Enter customer name:")
    if not name:
        return
    customer_id = str(len(data["customers"]) + 1)
    customer = Customer(name, customer_id)
    data["customers"][customer_id] = customer.to_dict()
    save_data()
    messagebox.showinfo("Success", f"Customer added with ID: {customer_id}")

def remove_customer():
    cid = simpledialog.askstring("Remove Customer", "Enter customer ID to remove:")
    if cid in data["customers"]:
        for acc_id in data["customers"][cid]["accounts"]:
            data["accounts"].pop(acc_id, None)
        data["customers"].pop(cid)
        save_data()
        messagebox.showinfo("Removed", f"Customer ID {cid} removed.")
    else:
        messagebox.showerror("Error", "Customer not found.")

def create_account():
    cid = simpledialog.askstring("Create Account", "Enter customer ID:")
    if cid not in data["customers"]:
        messagebox.showerror("Error", "Customer not found.")
        return
    acc_type = simpledialog.askstring("Account Type", "Enter account type (Savings/Checking):")
    if acc_type not in ["Savings", "Checking"]:
        messagebox.showerror("Error", "Invalid account type.")
        return
    acc_id = str(len(data["accounts"]) + 1001)
    account = BankAccount(acc_id, cid, acc_type)
    account_dict = account.to_dict()
    data["accounts"][acc_id] = account_dict
    data["customers"][cid]["accounts"].append(acc_id)
    save_data()
    messagebox.showinfo("Success", f"{acc_type} account created with number: {acc_id}")

def view_accounts():
    output = ""
    for acc_id, acc in data["accounts"].items():
        output += f"{acc_id} ({acc['acc_type']}): ₹{acc['balance']} [Owner ID: {acc['customer_id']}]\n"
    messagebox.showinfo("Accounts", output or "No accounts found.")

def deposit():
    acc_id = simpledialog.askstring("Deposit", "Enter account number:")
    amt_str = simpledialog.askstring("Deposit", "Enter amount:")
    if not acc_id or not amt_str:
        return
    try:
        amt = float(amt_str)
    except:
        messagebox.showerror("Error", "Invalid amount.")
        return
    if acc_id in data["accounts"]:
        data["accounts"][acc_id]["balance"] += amt
        data["accounts"][acc_id]["transactions"].append(f"Deposited ₹{amt}")
        save_data()
        messagebox.showinfo("Deposited", f"₹{amt} deposited.")
    else:
        messagebox.showerror("Error", "Account not found.")

def withdraw():
    acc_id = simpledialog.askstring("Withdraw", "Enter account number:")
    amt_str = simpledialog.askstring("Withdraw", "Enter amount:")
    if not acc_id or not amt_str:
        return
    try:
        amt = float(amt_str)
    except:
        messagebox.showerror("Error", "Invalid amount.")
        return
    if acc_id in data["accounts"]:
        acc = data["accounts"][acc_id]
        if acc["balance"] + acc.get("overdraft_limit", 0) >= amt:
            acc["balance"] -= amt
            acc["transactions"].append(f"Withdrew ₹{amt}")
            save_data()
            messagebox.showinfo("Success", f"₹{amt} withdrawn.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")
    else:
        messagebox.showerror("Error", "Account not found.")

def transfer():
    from_acc = simpledialog.askstring("Transfer", "From account:")
    to_acc = simpledialog.askstring("Transfer", "To account:")
    amt_str = simpledialog.askstring("Transfer", "Amount:")
    if not from_acc or not to_acc or not amt_str:
        return
    try:
        amt = float(amt_str)
    except:
        messagebox.showerror("Error", "Invalid amount.")
        return
    if from_acc in data["accounts"] and to_acc in data["accounts"]:
        if data["accounts"][from_acc]["balance"] + data["accounts"][from_acc].get("overdraft_limit", 0) >= amt:
            data["accounts"][from_acc]["balance"] -= amt
            data["accounts"][to_acc]["balance"] += amt
            data["accounts"][from_acc]["transactions"].append(f"Transferred ₹{amt} to {to_acc}")
            data["accounts"][to_acc]["transactions"].append(f"Received ₹{amt} from {from_acc}")
            save_data()
            messagebox.showinfo("Success", "Transfer complete.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")
    else:
        messagebox.showerror("Error", "Account not found.")

def apply_interest():
    for acc in data["accounts"].values():
        if acc["acc_type"] == "Savings":
            interest = acc["balance"] * 0.03
            acc["balance"] += interest
            acc["transactions"].append(f"Interest applied: ₹{round(interest, 2)}")
    save_data()
    messagebox.showinfo("Interest Applied", "3% interest applied to all savings accounts.")

def view_transactions():
    acc_id = simpledialog.askstring("Transaction History", "Enter account number:")
    if acc_id in data["accounts"]:
        txns = data["accounts"][acc_id].get("transactions", [])
        history = "\n".join(txns) if txns else "No transactions yet."
        messagebox.showinfo("Transaction History", history)
    else:
        messagebox.showerror("Error", "Account not found.")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Banking System")

btns = [
    ("Add Customer", add_customer),
    ("Remove Customer", remove_customer),
    ("Create Account", create_account),
    ("View Accounts", view_accounts),
    ("Deposit", deposit),
    ("Withdraw", withdraw),
    ("Transfer", transfer),
    ("Apply Interest (Savings)", apply_interest),
    ("View Transaction History", view_transactions),
]

for i, (text, cmd) in enumerate(btns):
    tk.Button(root, text=text, width=30, command=cmd).grid(row=i, column=0, padx=10, pady=5)

root.mainloop()
