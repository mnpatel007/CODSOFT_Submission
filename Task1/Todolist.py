import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pickle
import os

class Task:
    def __init__(self, description, due_date=None, priority="medium"):
        self.description = description
        self.completed = False
        self.due_date = due_date
        self.priority = priority

    def mark_completed(self):
        self.completed = True

    def time_remaining(self):
        if self.due_date:
            delta = self.due_date - datetime.now().date()
            if delta.days == 1:
                return f"{(delta.seconds // 3600):02d}:{(delta.seconds % 3600 // 60):02d} hours remaining"
            else:
                return f"{delta.days} days remaining"
        else:
            return "No due date"

    def __str__(self):
        due_date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No due date"
        return f"[{'x' if self.completed else ' '}] {self.description} (Due: {due_date_str}, Priority: {self.priority})"

class ToDoList:
    def __init__(self, filename="todo_list.pkl"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, description, due_date=None, priority="medium"):
        if not self.is_duplicate(description):
            self.tasks.append(Task(description, due_date, priority))
            self.save_tasks()
        else:
            messagebox.showerror("Error", f"A task with description '{description}' already exists.")

    def is_duplicate(self, description):
        for task in self.tasks:
            if task.description == description:
                return True
        return False

    def list_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()
        else:
            print("Invalid task number.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            print("Invalid task number.")

    def search_tasks(self, keyword):
        results = [task for task in self.tasks if keyword.lower() in task.description.lower()]
        return results

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        return []

    def save_tasks(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.tasks, file)

class ToDoApp(tk.Tk):
    def __init__(self, todo_list):
        super().__init__()
        self.todo_list = todo_list
        self.title("To-Do List Application")
        self.geometry("650x400")

        self.create_widgets()

    def create_widgets(self):
        self.task_listbox = tk.Listbox(self, height=15, width=50)
        self.task_listbox.pack(pady=10)

        self.add_frame = tk.Frame(self)
        self.add_frame.pack(pady=5)

        self.task_entry = tk.Entry(self.add_frame, width=30)
        self.task_entry.grid(row=0, column=0, padx=5)

        self.due_date_label = tk.Label(self.add_frame, text="Due Date:")
        self.due_date_label.grid(row=0, column=1, padx=5)

        self.due_date_entry = tk.Entry(self.add_frame, width=15)
        self.due_date_entry.grid(row=0, column=2, padx=5)
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.due_date_entry.bind("<Enter>", self.show_date_prompt)
        self.due_date_entry.bind("<Leave>", self.hide_date_prompt)

        self.priority_label = tk.Label(self.add_frame, text="Priority:")
        self.priority_label.grid(row=0, column=3, padx=5)

        self.priority_combobox = ttk.Combobox(self.add_frame, values=["high", "medium", "low"], width=10)
        self.priority_combobox.grid(row=0, column=4, padx=5)
        self.priority_combobox.set("medium")

        self.add_button = tk.Button(self.add_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=5, padx=5)

        self.complete_button = tk.Button(self, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list.tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        description = self.task_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_combobox.get().strip()

        if description:
            if due_date and due_date != "YYYY-MM-DD":
                try:
                    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due_date < datetime.now().date():
                        messagebox.showerror("Error", "Please enter a valid due date.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return
            else:
                due_date = None

            self.todo_list.add_task(description, due_date, priority)
            self.load_tasks()

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.todo_list.complete_task(task_index)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "No task selected.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.todo_list.delete_task(task_index)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "No task selected.")

    def show_date_prompt(self, event):
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.config(fg="gray")
        self.due_date_entry.insert(0, "YYYY-MM-DD")

    def hide_date_prompt(self, event):
        if self.due_date_entry.get() == "YYYY-MM-DD":
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.config(fg="black")
            self.due_date_entry.insert(0, "")

if __name__ == "__main__":
    todo_list = ToDoList()
    app = ToDoApp(todo_list)
    app.mainloop()
