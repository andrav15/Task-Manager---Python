import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_tasks, save_tasks
from datetime import datetime

sorted_tasks = []

def refresh_list():
    global sorted_tasks, progress
    tasks = load_tasks()
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority", "Low")))
    
    listbox.delete(0, tk.END)
    today = datetime.now()
    
    for i, t in enumerate(sorted_tasks):
        status = "✔" if t["done"] else "X"
        deadline = t.get("deadline")
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%d-%m-%Y")
                days_left = (deadline_date - today).days
                if t["done"]:
                    deadline_info = f"{deadline} (finalizat)"
                elif days_left < 0:
                    deadline_info = f"{deadline} (termen depășit)"
                else:
                    deadline_info = f"{deadline} ({days_left} zile rămase)"
            except:
                deadline_info = f"{deadline}"
        else:
            deadline_info = "Fără deadline"

        priority = t.get("priority", "N/A")
        
        color = "black"
        if t["done"]:
            color = "green"
        elif priority == "High":
            color = "red"
        elif priority == "Medium":
            color = "orange"
        elif priority == "Low":
            color = "blue"
        if deadline and days_left < 0 and not t["done"]:
            color = "red"

        listbox.insert(tk.END, f"{i+1}. {t['title']} [{status}] - {deadline_info} | {priority}")
        listbox.itemconfig(i, fg=color)

    total = len(sorted_tasks)
    if total == 0:
        progress["value"] = 0
    else:
        done_count = sum(1 for t in sorted_tasks if t["done"])
        percent = int((done_count / total) * 100)
        progress["value"] = percent


def add_task_gui():
    title = title_entry.get().strip()
    if not title:
        messagebox.showwarning("Atenție", "Scrie un titlu pentru task!")
        return
    
    deadline = deadline_entry.get().strip()
    priority = priority_var.get()

    tasks = load_tasks()
    tasks.append({"title": title, "done": False, "deadline": deadline if deadline else None, "priority": priority})
    save_tasks(tasks)

    title_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    refresh_list()

def delete_task_gui():
    try:
        idx = listbox.curselection()[0]
        task_to_delete = sorted_tasks[idx]
        tasks = load_tasks()
        tasks.remove(task_to_delete)
        save_tasks(tasks)
        refresh_list()
    except IndexError:
        messagebox.showwarning("Atenție", "Selectează un task din listă!")

def toggle_done_gui():
    try:
        idx = listbox.curselection()[0]
        task_to_toggle = sorted_tasks[idx]
        tasks = load_tasks()
        for t in tasks:
            if t == task_to_toggle:
                t["done"] = not t["done"]
                break
        save_tasks(tasks)
        refresh_list()
    except IndexError:
        messagebox.showwarning("Atenție", "Selectează un task din listă!")

root = tk.Tk()
root.title("Task Manager GUI")

tk.Label(root, text="Titlu:").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(root, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Deadline (ZZ-LL-AAAA):").grid(row=1, column=0, padx=5, pady=5)
deadline_entry = tk.Entry(root, width=30)
deadline_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Prioritate:").grid(row=2, column=0, padx=5, pady=5)
priority_var = tk.StringVar(value="Low")
tk.OptionMenu(root, priority_var, "Low", "Medium", "High").grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Adaugă task", command=add_task_gui).grid(row=3, column=0, columnspan=2, pady=5)

listbox = tk.Listbox(root, width=70)
listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

tk.Button(root, text="Schimbă status", command=toggle_done_gui).grid(row=5, column=0, pady=5)
tk.Button(root, text="Șterge task", command=delete_task_gui).grid(row=5, column=1, pady=5)

progress_label = tk.Label(root, text="Progres taskuri:")
progress_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.grid(row=6, column=1, padx=5, pady=5)

refresh_list()

root.mainloop()
