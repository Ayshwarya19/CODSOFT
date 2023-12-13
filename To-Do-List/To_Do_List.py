import tkinter
from tkinter import messagebox
import pickle
from datetime import datetime

class ToDoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        self.create_widgets()

    def create_widgets(self):
        # Create task frame
        self.frame_tasks = tkinter.Frame(self.master)
        self.frame_tasks.pack()

        self.listbox_tasks = tkinter.Listbox(self.frame_tasks, height=10, width=50)
        self.listbox_tasks.pack(side=tkinter.LEFT)

        self.scrollbar_tasks = tkinter.Scrollbar(self.frame_tasks)
        self.scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.listbox_tasks.config(yscrollcommand=self.scrollbar_tasks.set)
        self.scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # Create entry and buttons
        self.entry_task = tkinter.Entry(self.master, width=50)
        self.entry_task.pack()

        self.button_add_task = tkinter.Button(self.master, text="Add task", width=48, command=self.add_task)
        self.button_add_task.pack()

        self.button_delete_task = tkinter.Button(self.master, text="Delete task", width=48, command=self.delete_task)
        self.button_delete_task.pack()

        self.button_load_tasks = tkinter.Button(self.master, text="Load tasks", width=48, command=self.load_tasks)
        self.button_load_tasks.pack()

        self.button_save_tasks = tkinter.Button(self.master, text="Save tasks", width=48, command=self.save_tasks)
        self.button_save_tasks.pack()

    def add_task(self):
        task = self.entry_task.get()
        if task != "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_with_timestamp = f"{timestamp} - {task}"
            self.listbox_tasks.insert(tkinter.END, task_with_timestamp)
            self.entry_task.delete(0, tkinter.END)
        else:
            messagebox.showwarning(title="Warning!", message="You must enter a task.")

    def delete_task(self):
        try:
            selected_index = self.listbox_tasks.curselection()[0]
            selected_task = self.listbox_tasks.get(selected_index)
            confirmation = messagebox.askokcancel("Confirm Deletion", f"Delete the task:\n{selected_task}")
            if confirmation:
                self.listbox_tasks.delete(selected_index)
        except IndexError:
            messagebox.showwarning(title="Warning!", message="You must select a task.")

    def load_tasks(self):
        try:
            with open("tasks.dat", "rb") as file:
                tasks = pickle.load(file)
            self.listbox_tasks.delete(0, tkinter.END)
            for task in tasks:
                self.listbox_tasks.insert(tkinter.END, task)
        except FileNotFoundError:
            messagebox.showwarning(title="Warning!", message="Cannot find tasks.dat.")

    def save_tasks(self):
        tasks = self.listbox_tasks.get(0, tkinter.END)
        with open("tasks.dat", "wb") as file:
            pickle.dump(tasks, file)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = ToDoApp(root)
    root.mainloop()
