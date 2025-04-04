import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

class InventoryItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login - Inventory Management")
        self.root.geometry("300x200")
        self.on_success = on_success
        
        self.valid_credentials = {"username": "admin", "password": "password123"}
        
        self.login_frame = ttk.Frame(root, padding="20")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.login_frame, text="Login", command=self.attempt_login).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.root.bind('<Return>', lambda event: self.attempt_login())

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if (username == self.valid_credentials["username"] and 
            password == self.valid_credentials["password"]):
            self.login_frame.destroy()
            self.root.unbind('<Return>')
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.password_entry.delete(0, tk.END)

class InventoryManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        
        self.inventory = {}
        
        # Create main frames with background color
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.input_frame.configure(style="Input.TFrame")
        
        self.display_frame = ttk.Frame(root, padding="10")
        self.display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.display_frame.configure(style="Display.TFrame")
        
        # Style configuration for colors
        style = ttk.Style()
        style.configure("Input.TFrame", background="#f0f0f0")
        style.configure("Display.TFrame", background="#e0e0e0")
        style.configure("TButton", padding=5)
        
        # Input fields
        ttk.Label(self.input_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.input_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.input_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.input_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons with colors
        ttk.Button(self.input_frame, text="Add Item", command=self.add_item, style="Success.TButton").grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Remove Item", command=self.remove_item, style="Danger.TButton").grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Update Price", command=self.update_price, style="Info.TButton").grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Clear Fields", command=self.clear_fields).grid(row=3, column=3, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Generate Report", command=self.generate_report, style="Report.TButton").grid(row=3, column=4, padx=5, pady=5)
        
        style.configure("Success.TButton", background="#90ee90")  # Light green
        style.configure("Danger.TButton", background="#ff9999")   # Light red
        style.configure("Info.TButton", background="#87cefa")    # Light blue
        style.configure("Report.TButton", background="#ffd700")  # Gold
        
        # Inventory display
        self.tree = ttk.Treeview(self.display_frame, columns=("Name", "Quantity", "Price", "Total"), show="headings")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price ($)")
        self.tree.heading("Total", text="Total Value ($)")
        self.tree.grid(row=0, column=0, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Total value label with color
        self.total_label = ttk.Label(self.display_frame, text="Total Inventory Value: $0.00", foreground="#006400")  # Dark green
        self.total_label.grid(row=1, column=0, pady=5)

    def add_item(self):
        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            
            if name and quantity >= 0 and price >= 0:
                if name in self.inventory:
                    self.inventory[name].quantity += quantity
                else:
                    self.inventory[name] = InventoryItem(name, quantity, price)
                self.update_display()
                messagebox.showinfo("Success", f"Added {quantity} {name}(s) to inventory")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Please enter valid values")
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values for quantity and price")

    def remove_item(self):
        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            
            if name in self.inventory:
                if self.inventory[name].quantity >= quantity:
                    self.inventory[name].quantity -= quantity
                    if self.inventory[name].quantity == 0:
                        del self.inventory[name]
                    self.update_display()
                    messagebox.showinfo("Success", f"Removed {quantity} {name}(s) from inventory")
                    self.clear_fields()
                else:
                    messagebox.showerror("Error", f"Not enough {name} in inventory")
            else:
                messagebox.showerror("Error", f"{name} not found in inventory")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric value for quantity")

    def update_price(self):
        try:
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            
            if name in self.inventory:
                self.inventory[name].price = price
                self.update_display()
                messagebox.showinfo("Success", f"Updated price of {name} to ${price:.2f}")
                self.clear_fields()
            else:
                messagebox.showerror("Error", f"{name} not found in inventory")
        except ValueError:
            messagebox.showerror("Error", "Please enter a numeric value for price")

    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_value = 0
        for item in self.inventory.values():
            total = item.quantity * item.price
            self.tree.insert("", "end", values=(item.name, item.quantity, f"{item.price:.2f}", f"{total:.2f}"))
            total_value += total
        
        self.total_label.config(text=f"Total Inventory Value: ${total_value:.2f}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def generate_report(self):
        if not self.inventory:
            messagebox.showinfo("Report", "Inventory is empty. No report generated.")
            return
        
        # Create report content
        report = "Inventory Report\n"
        report += f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "-" * 50 + "\n"
        report += f"{'Item Name':<20} {'Quantity':<10} {'Price ($)':<12} {'Total ($)':<12}\n"
        report += "-" * 50 + "\n"
        
        total_value = 0
        for item in self.inventory.values():
            total = item.quantity * item.price
            total_value += total
            report += f"{item.name:<20} {item.quantity:<10} {item.price:<12.2f} {total:<12.2f}\n"
        
        report += "-" * 50 + "\n"
        report += f"Total Inventory Value: ${total_value:.2f}\n"
        
        # Show colored preview
        self.show_report_preview(report)
        
        # Save to file (plain text)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inventory_report_{timestamp}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(report)
            messagebox.showinfo("Report Generated", f"Report saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def show_report_preview(self, report):
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Report Preview")
        preview_window.geometry("600x400")
        
        # ScrolledText widget for report display
        report_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, width=70, height=20, bg="#f0f8ff")  # Alice blue background
        report_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Insert report with colors
        lines = report.split('\n')
        for line in lines:
            if "Inventory Report" in line:
                report_text.insert(tk.END, line + "\n", "header")
            elif "Generated on" in line:
                report_text.insert(tk.END, line + "\n", "timestamp")
            elif "Item Name" in line:
                report_text.insert(tk.END, line + "\n", "columns")
            elif "Total Inventory Value" in line:
                report_text.insert(tk.END, line + "\n", "total")
            elif line.strip() == "-" * 50:
                report_text.insert(tk.END, line + "\n", "separator")
            else:
                report_text.insert(tk.END, line + "\n")
        
        # Configure tags for colors
        report_text.tag_configure("header", foreground="#00008b", font=("Arial", 12, "bold"))  # Dark blue
        report_text.tag_configure("timestamp", foreground="#006400")  # Dark green
        report_text.tag_configure("columns", foreground="#8b0000", font=("Arial", 10, "bold"))  # Dark red
        report_text.tag_configure("total", foreground="#2f0047", font=("Arial", 10, "bold"))  # Dark purple
        report_text.tag_configure("separator", foreground="#808080")  # Grey
        
        report_text.config(state="disabled")  # Make it read-only

def main():
    root = tk.Tk()
    
    def start_inventory():
        inventory_app = InventoryManagementGUI(root)
    
    login_app = LoginPage(root, start_inventory)
    root.mainloop()

if __name__ == "__main__":
    main()