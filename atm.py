import tkinter as tk
from tkinter import messagebox, simpledialog

class ATM:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM Machine")
        self.master.geometry("400x500")
        self.master.configure(bg="white")

        # Hardcoded PIN and initial balance
        self.pin = 1234
        self.balance = 1000.0

        self.is_authenticated = False
        self.minimum_withdrawal = 500.0
        
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Welcome to Your Bank", bg="white", fg="black", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=20)

        self.pin_label = tk.Label(self.master, text="Enter your PIN:", bg="white", fg="black", font=("Arial", 14))
        self.pin_label.pack(pady=10)

        self.pin_entry = tk.Entry(self.master, show='*', font=("Arial", 14))
        self.pin_entry.pack(pady=10)

        self.login_label = self.create_label("Login", self.authenticate_user, "black", "lightgray")
        self.login_label.pack(pady=10)

        # Action buttons (initially hidden)
        self.action_buttons = []
        self.action_buttons.append(self.create_label("Show Balance", self.show_balance, "black", "lightgray"))
        self.action_buttons.append(self.create_label("Deposit", self.deposit, "black", "lightgray"))
        self.action_buttons.append(self.create_label("Withdraw", self.withdraw, "black", "lightgray"))
        self.action_buttons.append(self.create_label("Transfer", self.transfer, "black", "lightgray"))
        self.action_buttons.append(self.create_label("Exit", self.master.quit, "black", "lightgray"))

        for button in self.action_buttons:
            button.pack(pady=10)
            button.pack_forget()  # Hide buttons initially

    def create_label(self, text, command, bg_color, hover_color):
        label = tk.Label(self.master, text=text, bg=bg_color, fg="black", width=20, height=2, font=("Arial", 12), relief="raised")
        label.bind("<Button-1>", lambda e: command())
        label.bind("<Enter>", lambda e: label.config(bg=hover_color))
        label.bind("<Leave>", lambda e: label.config(bg=bg_color))
        return label

    def authenticate_user(self):
        entered_pin = self.pin_entry.get()
        if entered_pin.isdigit() and int(entered_pin) == self.pin:
            self.is_authenticated = True
            self.pin_label.config(text="Authentication successful.")
            self.pin_entry.config(state=tk.DISABLED)
            for button in self.action_buttons:
                button.pack()  # Show buttons after successful login
        else:
            messagebox.showerror("Error", "Incorrect PIN. Please try again.")

    def show_balance(self):
        messagebox.showinfo("Current Balance", f"Your current balance is: ₹{self.balance:.2f}")

    def deposit(self):
        amount = self.get_amount("Enter amount to deposit:")
        if amount is not None:
            self.balance += amount
            messagebox.showinfo("Success", f"₹{amount:.2f} deposited successfully.")

    def withdraw(self):
        amount = self.get_amount("Enter amount to withdraw:")
        if amount is not None:
            if amount < self.minimum_withdrawal:
                messagebox.showerror("Error", f"Minimum withdrawal amount is ₹{self.minimum_withdrawal:.2f}.")
            elif self.balance - amount < 0:
                messagebox.showerror("Error", "Insufficient funds for withdrawal.")
            else:
                self.balance -= amount
                messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn successfully.")

    def transfer(self):
        account_number = simpledialog.askstring("Input", "Enter the account number to transfer to:")
        if account_number and self.validate_account_number(account_number):
            amount = self.get_amount("Enter amount to transfer:")
            if amount is not None:
                if amount < self.minimum_withdrawal:
                    messagebox.showerror("Error", f"Minimum transfer amount is ₹{self.minimum_withdrawal:.2f}.")
                elif self.balance - amount < 0:
                    messagebox.showerror("Error", "Insufficient funds for transfer.")
                else:
                    self.balance -= amount
                    messagebox.showinfo("Success", f"₹{amount:.2f} transferred to account {account_number} successfully.")
        else:
            messagebox.showerror("Error", "Invalid account number. Please enter a valid account number.")

    def validate_account_number(self, account_number):
        return account_number.isdigit()

    def get_amount(self, prompt):
        amount_str = simpledialog.askstring("Input", prompt)
        if amount_str is not None:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                return amount
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
                return None
        return None

if __name__ == "__main__":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
