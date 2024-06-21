import tkinter as tk
from tkinter import ttk
import urllib.request
from PIL import Image, ImageTk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Calculator")

        # Download background image from the internet
        url = "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max"
        urllib.request.urlretrieve(url, "background.jpg")

        # Load background image
        background_image = Image.open("background.jpg")
        background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(background_image)  # Keep a reference to avoid garbage collection

        # Create background label
        background_label = tk.Label(master, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Display
        self.display = tk.Entry(master, width=40, borderwidth=5, font=('Arial', 24), bg='lightgray', fg='black')
        self.display.grid(row=0, column=0, columnspan=6, padx=5, pady=5)

        # Buttons
        buttons = [
            '7', '8', '9', '/', 'sin', 'cos',
            '4', '5', '6', '*', 'tan', 'log',
            '1', '2', '3', '-', 'exp', 'sqrt',
            '0', '.', '=', '+', 'x²', 'x³',
            '(', ')', 'C', '←', '1/x', '1/2'
        ]

        row = 1
        col = 0
        for button_text in buttons:
            button = tk.Button(master, text=button_text, width=8, height=2, command=lambda text=button_text: self.button_click(text),
                               font=('Helvetica', 18), bg='lightblue', fg='black', activebackground='skyblue', activeforeground='black')
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            col += 1
            if col > 5:
                col = 0
                row += 1

        # Resize columns for uniform button size
        for i in range(6):
            master.columnconfigure(i, weight=1)

        # Focus on display entry
        self.display.focus_set()

        # Bind keyboard events
        master.bind('<Key>', self.key_press)

    def button_click(self, text):
        if text == '=':
            try:
                expression = self.display.get()
                expression = expression.replace('sin', 'math.sin')
                expression = expression.replace('cos', 'math.cos')
                expression = expression.replace('tan', 'math.tan')
                expression = expression.replace('log', 'math.log')
                expression = expression.replace('exp', 'math.exp')
                expression = expression.replace('sqrt', 'math.sqrt')
                expression = expression.replace('x²', '**2')
                expression = expression.replace('x³', '**3')
                expression = expression.replace('1/2', '/2')
                expression = expression.replace('1/x', '1/')
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, 'Error')
        elif text == '←':
            self.display.delete(len(self.display.get()) - 1, tk.END)
        elif text == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, text)

    def key_press(self, event):
        text = event.char
        if text in '0123456789+-*/().':
            self.display.insert(tk.END, text)
        elif text == '=' or text == '\r':
            self.button_click('=')
        elif text == '\b':
            self.button_click('←')

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()
