import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        # Create input field
        self.input_entry = ttk.Entry(root, width=50, font=('Arial', 14), foreground='#000000')
        self.input_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Create buttons with custom styling
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('(', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), (')', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('^', 5, 3),
            ('clear', 6, 0), ('exit', 6, 1), ('⌫', 6, 2)
        ]

        for (text, row, col) in buttons:
            button = ttk.Button(root, text=text, command=lambda t=text: self.on_button_click(t), width=10, style='Calc.TButton')
            button.grid(row=row, column=col, padx=5, pady=5)

        # Custom style for buttons
        root.tk_setPalette(background='#333333', foreground='#ffffff', activeBackground='#666666', activeForeground='#ffffff')
        root.option_add('*TButton*font', ('Arial', 12))
        root.option_add('*TButton*borderWidth', 2)
        root.option_add('*TButton*relief', 'raised')
        root.option_add('*TButton*padding', 10)
        root.option_add('*TButton*background', '#444444')
        root.option_add('*TButton*foreground', '#ffffff')
        root.option_add('*TButton*highlightColor', '#666666')
        root.option_add('*TButton*highlightBackground', '#666666')

    def on_button_click(self, text):
        if text == '=':
            expression = self.input_entry.get()
            try:
                result = eval(expression)
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(tk.END, str(result))
            except Exception as e:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(tk.END, "Error")
        elif text == 'clear':
            self.input_entry.delete(0, tk.END)
        elif text == 'exit':
            self.root.destroy()
        elif text == '⌫':  # Backspace functionality
            current_text = self.input_entry.get()
            if len(current_text) > 0:
                self.input_entry.delete(len(current_text) - 1, tk.END)
        else:
            self.input_entry.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure('Calc.TButton', font=('Arial', 12))
    app = Calculator(root)
    root.mainloop()
