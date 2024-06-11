import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string

class AdvancedPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x400")
        self.root.configure(background='#2d2d2d')

        # Title label
        title_label = tk.Label(root, text="Password Generator", font=('Helvetica', 24, 'bold'), bg='#2d2d2d', fg='#ffffff')
        title_label.pack(pady=20)

        # Length selection
        length_label = tk.Label(root, text="Password Length:", font=('Helvetica', 14), bg='#2d2d2d', fg='#ffffff')
        length_label.pack(pady=10)
        self.length_entry = ttk.Entry(root, width=5, font=('Helvetica', 14))
        self.length_entry.pack()

        # Complexity selection
        self.var_uppercase = tk.IntVar()
        self.var_digits = tk.IntVar()
        self.var_special = tk.IntVar()

        check_uppercase = tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.var_uppercase, font=('Helvetica', 12), bg='#2d2d2d', fg='#ffffff', selectcolor='#444444')
        check_uppercase.pack(pady=5)

        check_digits = tk.Checkbutton(root, text="Include Digits", variable=self.var_digits, font=('Helvetica', 12), bg='#2d2d2d', fg='#ffffff', selectcolor='#444444')
        check_digits.pack(pady=5)

        check_special = tk.Checkbutton(root, text="Include Special Characters (@, _)", variable=self.var_special, font=('Helvetica', 12), bg='#2d2d2d', fg='#ffffff', selectcolor='#444444')
        check_special.pack(pady=5)

        # Generate button
        generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password, style='Custom.TButton')
        generate_button.pack(pady=20)

        # Password display
        self.password_display = tk.Label(root, text="", font=('Helvetica', 16, 'bold'), bg='#2d2d2d', fg='#ffffff', wraplength=400)
        self.password_display.pack(pady=20)

        # Custom style for the button
        style = ttk.Style()
        style.configure('Custom.TButton', font=('Helvetica', 14), padding=10)

    def generate_password(self):
        print("Generate button clicked")  # Debug statement
        length = self.length_entry.get()
        if not length.isdigit() or int(length) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the password length.")
            return

        length = int(length)
        characters = string.ascii_lowercase
        if self.var_uppercase.get():
            characters += string.ascii_uppercase
        if self.var_digits.get():
            characters += string.digits
        if self.var_special.get():
            characters += '@_'

        if not characters:
            messagebox.showerror("No Character Set Selected", "Please select at least one character set.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_display.config(text=password)
        print(f"Generated Password: {password}")  # Debug statement
        messagebox.showinfo("Generated Password", f"Your generated password is: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordGenerator(root)
    root.mainloop()
