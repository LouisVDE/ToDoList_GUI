import tkinter as tk
from tkinter import messagebox

def update_language():
    tasks_menu.delete(0, tk.END)
    if current_language == "fr":
        tasks_menu.add_command(label="Tâches actives", command=switch_to_active_tasks)
        tasks_menu.add_command(label="Tâches complétées", command=switch_to_completed_tasks)
        add_button.config(text="Ajouter")
        remove_button.config(text="Supprimer")
    else:
        tasks_menu.add_command(label="Active Tasks", command=switch_to_active_tasks)
        tasks_menu.add_command(label="Completed Tasks", command=switch_to_completed_tasks)
        add_button.config(text="Add")
        remove_button.config(text="Remove")

def set_french():
    global current_language
    current_language = "fr"
    window.config(menu=menu)
    update_language()

def set_english():
    global current_language
    current_language = "en"
    window.config(menu=menu)
    update_language()

def add_task(event=None):
    task = entry.get()
    if task:
        tasks.append(task)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()

def remove_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        if current_list == "active":
            completed_task = tasks.pop(index)
            tasks_completed.append(completed_task)
            listbox.delete(index)
            save_tasks()
            save_completed_task(completed_task)
        elif current_list == "completed":
            tasks_completed.pop(index)
            listbox.delete(index)
            save_completed_tasks()

def switch_to_active_tasks():
    global current_list
    current_list = "active"
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

def switch_to_completed_tasks():
    global current_list
    current_list = "completed"
    listbox.delete(0, tk.END)
    for task in tasks_completed:
        listbox.insert(tk.END, task)

def delete_completed_task():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        tasks_completed.pop(index)
        listbox.delete(index)
        save_completed_tasks()
        completed_tasks_menu.delete(0, tk.END)
        for i, task in enumerate(tasks_completed):
            completed_tasks_menu.add_command(label=task, command=lambda i=i: delete_completed_task_menu(i))

def delete_completed_task_menu(index):
    tasks_completed.pop(index)
    listbox.delete(index)
    save_completed_tasks()

def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

def save_completed_task(task):
    with open("tasks_completed.txt", "a") as file:
        file.write(task + "\n")

def save_completed_tasks():
    with open("tasks_completed.txt", "w") as file:
        for task in tasks_completed:
            file.write(task + "\n")

def load_tasks():
    tasks = []
    with open("tasks.txt", "r") as file:
        for line in file:
            tasks.append(line.strip())
    return tasks

def load_completed_tasks():
    tasks_completed = []
    with open("tasks_completed.txt", "r") as file:
        for line in file:
            tasks_completed.append(line.strip())
    return tasks_completed

def on_resize(event):
    listbox.config(width=event.width // 10, height=event.height // 25)

window = tk.Tk()
window.title("To-Do List V1.0")
window.geometry("800x600")

tasks = load_tasks()
tasks_completed = load_completed_tasks()
current_list = "active"
current_language = "fr"

listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand=True)

entry = tk.Entry(window)
entry.pack()
add_button = tk.Button(window, text="Ajouter", command=add_task)
add_button.pack()
remove_button = tk.Button(window, text="Supprimer", command=remove_task)
remove_button.pack()

menu = tk.Menu(window)
window.config(menu=menu)

tasks_menu = tk.Menu(menu)
menu.add_cascade(label="Tâches", menu=tasks_menu)

language_menu = tk.Menu(menu)
menu.add_cascade(label="Langue", menu=language_menu)
language_menu.add_command(label="Français", command=set_french)
language_menu.add_command(label="English", command=set_english)

completed_tasks_menu = tk.Menu(menu)
completed_tasks_menu.add_command(label="Supprimer tâche", command=delete_completed_task)

update_language()

window.bind("<Configure>", on_resize)
window.bind("<Return>", add_task)

window.mainloop()
