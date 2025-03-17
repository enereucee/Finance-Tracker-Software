# Import Tkinter
import tkinter as tk
from tkinter import ttk, messagebox


# Create the Main Application Window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("650x600")


# List to Store Transactions
transactions = []


# Form/Create the Heading Frame
title_frame = tk.Frame(root, bg="light blue", pady=10)
title_frame.pack(fill="x")

# Heading Label
title_label = tk.Label(title_frame, text="PERSONAL FINANCE TRACKER", font=("Tahoma", 20, "bold"), fg="white", bg="light blue")
title_label.pack()


# Function to Save Transaction
def save_transaction():
    t_type = type_var.get().strip()
    category = category_var.get().strip()
    amount = amount_entry.get().strip()
    date = date_entry.get().strip()

    # Input validation
    if not amount or not date or category == "" or t_type == "":
        messagebox.showerror("Input Error", "All fields are required!")
        return

    if category == "Select Category":
        messagebox.showerror("Input Error", "Please select a valid category!")
        return

    try:
        amount = float(amount)  # Convert amount to a number
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid amount!")
        return


    # Store Transaction as a Dictionary
    transaction = {"type": t_type, "category": category, "amount": amount, "date": date}
    transactions.append(transaction)
    

    # Update the table with the new transaction
    update_transaction_table()

    messagebox.showinfo("Success", "Transaction saved successfully!")
    clear_fields()


# Function to clear input fields after saving
def clear_fields():
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    category_var.set("Select Category")
    type_var.set("Income")


# Function to Update the Transaction Table
def update_transaction_table():
    # Clear existing data in the table
    for row in transaction_table.get_children():
        transaction_table.delete(row)

    # Insert new data
    for trans in transactions:
        transaction_table.insert("", "end", values=(trans["type"], trans["category"], trans["amount"], trans["date"]))


# Function to Delete a Selected Transaction
def delete_transaction():
    selected_item = transaction_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a transaction to delete!")
        return

    # Get selected item index
    item = transaction_table.item(selected_item)
    values = item["values"]

    # Find and remove the transaction from the list
    for trans in transactions:
        if list(trans.values()) == values:
            transactions.remove(trans)
            break

    # Update the table and summary
    update_transaction_table()
    update_summary()

    

# Function to Edit a Selected Transaction
def edit_transaction():
    selected_item = transaction_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a transaction to edit!")
        return

    # Get selected item index
    item = transaction_table.item(selected_item)
    values = item["values"]

    # Find the transaction in the list
    for trans in transactions:
        if list(trans.values()) == values:
            # Fill the input fields with selected transaction details
            type_var.set(trans["type"])
            category_var.set(trans["category"])
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, trans["amount"])
            date_entry.delete(0, tk.END)
            date_entry.insert(0, trans["date"])

            # Remove the selected transaction from the list
            transactions.remove(trans)
            break

    # Update the table to reflect removal before editing and Summary
    update_transaction_table()
    update_summary()



# Function to Add a New Transaction
def add_transaction():
    trans_type = type_var.get().strip()
    category = category_var.get().strip()
    amount_text = amount_entry.get().strip()
    date = date_entry.get().strip()

    # Validate inputs
    if not trans_type or not category or not amount_text or not date:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError                # Ensure amount is positive
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

    # Add transaction to list
    transaction.append({"type": trans_type, "category": category, "amount": amount, "date": date})
    update_transaction_table()
    messagebox.showinfo("Success", "Transaction added successfully!")

    # Clear input field
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

    

# Function to Calculate and Update Summary
def update_summary():
    total_income = sum(trans["amount"] for trans in transactions if trans["type"] == "Income")
    total_expense = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")
    balance = total_income - total_expense

    income_label.config(text=f"Total Income: \u20A6{total_income:.2f}")
    expense_label.config(text=f"Total Expense: \u20A6{total_expense:.2f}")
    balance_label.config(text=f"Balance: \u20A6{balance:.2f}")


# Function to Filter Transactions by Category
def filter_transactions():
    selected_category = filter_var.get()

    # Clear the table before inserting filtered transactions
    for row in transaction_table.get_children():
        transaction_table.delete(row)

    # Show transactions that match the selected category
    for trans in transactions:
        if trans["category"] == selected_category or selected_category == "All":
            transaction_table.insert("", "end", values=(trans["type"], trans["category"], trans["amount"], trans["date"]))

            
# Function to Sort Transactions
def sort_transactions():
    sort_by = sort_var.get()
    order = order_var.get()

    if sort_by == "Date":
        key_func = lambda trans: trans["date"]
    elif sort_by == "Category":
        key_func = lambda trans: trans["category"]
    elif sort_by == "Amount":
        key_func = lambda trans: trans["amount"]
    else:
        rturn       # Do nothing is no valid sort option is selected

    # Sort transactions based on the selected order
    reverse_order = True if order == "Descending" else False
    sorted_transactions = sorted(transactions, key=key_func, reverse=reverse_order)

    # Clear and update the table with sorted transanctions
    for row in transaction_table.get_children():
        transaction_table.delete(row)


    for trans in sorted_transactions:
        transaction_table.insert("", "end", values=(trans["type"], trans["category"], trans["amount"], trans["date"]))
        
        
# Function to Reset the Filter and Show all Transactions
def reset_filter():
    filter_var.set("All")
    update_transaction_table()

    
# Set a budget limit for expenses
budget_limit = 50000.00 


# Function to Check Budget and Alert the User
def check_budget():
    try:
        budget_limit = float(budget_entry.get())
        total_expenses = sum(trans["amount"] for trans in transactions if trans["type"] == "Expense")

        if total_expenses > budget_limit:
            messagebox.showwarning("Budget Alert", f"Warning! Your Total expenses ({total_expenses}) have exceeded the budget limit ({budget_limit}).")
        else:
            messagebox.showinfo("Budget Check", f"You're in line with budget! Total expenses: {total_expenses}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the budget limit.")



# Function to Clear All Transactions
def clear_all_transactions():
    global transactions
    transactions = []           # Reset transaction list

    # Clear table
    for row in transactions_table.get_children():
        transaction_table.delete(row)

    messagebox.showinfo("Clear All", "All transactions have been cleared!")

    
    
# Apply Styling to Labels, Buttons, and Entry Fields
for widget in root.winfo_children():
    if isinstance(widget, tk.Frame):
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                child.config(font=("Arial", 10, "bold"), padx=10, pady=5, relief="raised")
            elif isinstance(child, tk.Label):
                child.config(font=("Arial", 10, "bold"))
            elif isinstance(child, tk.Entry):
                child.config(font=("Arial", 10))
                
                
# Frame for transaction inputs
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)


# Frame for Category Filter
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)


# Filter Label
tk.Label(filter_frame, text="Filter by Category:").grid(row=0, column=0, padx=5)


# Frame for Sorting Options
sort_frame = tk.Frame(root)
sort_frame.pack(pady=10)


# Sort Label
tk.Label(sort_frame, text="Sort By:").grid(row=0, column=0, padx=5)



# Frame for Budget Input
budget_frame = tk.Frame(root)
budget_frame.pack(pady=10)


# Budget Limit Label
tk.Label(budget_frame, text="Set Budget Limit:").grid(row=0, column=0, padx=5)


# Transaction Type (Income or Expense)
tk.Label(frame, text="Transaction Type:").grid(row=0, column=0, padx=5, pady=5)
type_var = tk.StringVar()
type_dropdown = ttk.Combobox(frame, textvariable=type_var, values=["Income", "Expense"])
type_dropdown.grid(row=0, column=1, padx=5, pady=5)
type_dropdown.current(0)  # Set default value


# Category Dropdown
tk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=["Food", "Transport", "Rent", "Entertainment", "Shopping", "Salary", "Others"])
category_dropdown.grid(row=1, column=1, padx=5, pady=5)
category_dropdown.set("Select Category")  # Set default value


# Filter Dropdown
filter_var = tk.StringVar()
filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_var, values=["All", "Food", "Transport", "Rent", "Entertainment", "Shopping", "Salary", "Others"])
filter_dropdown.grid(row=0, column=1, padx=5)
filter_dropdown.set("All")


# Sort By Dropdown
sort_var = tk.StringVar()
sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_var, values=["Date", "Category", "Amount"])
sort_dropdown.grid(row=0, column=1, padx=5)
sort_dropdown.set("Date")


# Order Dropdown (Ascending/Descending)
order_var = tk.StringVar()
order_dropdown = ttk.Combobox(sort_frame, textvariable=order_var, values=["Ascending", "Descending"])
order_dropdown.grid(row=0, column=2, padx=5)
order_dropdown.set("Ascending")


# Budget Limit Entry
budget_entry = tk.Entry(budget_frame)
budget_entry.grid(row=0, column=1, padx=5)


# Amount Entry
tk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)


# Date Entry
tk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=3, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=3, column=1, padx=5, pady=5)


# Save Transaction Button
save_button = tk.Button(frame, text="Save Transaction", command=save_transaction, bg="green", fg="white")
save_button.grid(row=4, column=0, columnspan=2, pady=10)


# Table for Displaying Transactions 
columns = ("ID", "Type", "Category", "Amount", "Date")
transaction_table = ttk.Treeview(root, columns=columns, show="headings", height=6)
transaction_table.heading("ID", text="ID")
transaction_table.heading("Type", text="Type")
transaction_table.heading("Category", text="Category")
transaction_table.heading("Amount", text="Amount")
transaction_table.heading("Date", text="Date")


# Add Table to the Window
transaction_table.pack(pady=10)


# Summary Dashboard Labels
summary_frame = tk.Frame(root)
summary_frame.pack(pady=10)

income_label = tk.Label(summary_frame, text="Total Income: \u20A6 0.00", font=("Arial", 12, "bold"))
income_label.grid(row=0, column=0, padx=10)

expense_label = tk.Label(summary_frame, text="Total Expense: \u20A6 0.00", font=("Arial", 12, "bold"))
expense_label.grid(row=0, column=1, padx=10)

balance_label = tk.Label(summary_frame, text="Balance: \u20A6 0.00", font=("Arial", 12, "bold"), fg="blue")
balance_label.grid(row=0, column=2, padx=10)


# Buttons for Edit and Delete
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

edit_button = tk.Button(btn_frame, text="Edit Transaction", command=edit_transaction, bg="blue", fg="white")
edit_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(btn_frame, text="Delete Transaction", command=delete_transaction, bg="red", fg="white")
delete_button.grid(row=0, column=1, padx=10)


# Filter Button
filter_button = tk.Button(filter_frame, text="Filter", command=filter_transactions, bg="purple", fg="white")
filter_button.grid(row=0, column=2, padx=5)


# Reset Filter Button
reset_button = tk.Button(filter_frame, text="Reset", command=reset_filter, bg="navy blue", fg="white")
reset_button.grid(row=0, column=3, padx=5)
                         

# Sort Button
sort_button = tk.Button(sort_frame, text="Sort", command=sort_transactions, bg="orange", fg="white")
sort_button.grid(row=0, column=3, padx=5)


#Check Budget Button
budget_button = tk.Button(budget_frame, text="Check Budget", command=check_budget, bg="red", fg="white")
budget_button.grid(row=0, column=2, padx=5)


# Clear All Transaction Button
clear_all_button = tk.Button(root, text="Clear All Transactions", command=clear_all_transactions, bg="red", fg="white")
clear_all_button.pack(pady=10)



# Run the Tkinter main event loop
root.mainloop()
