import json
import os
from datetime import datetime
FILE_PATH = "tasks.json"

def load_tasks():
    """Încarcă task-urile din fișierul JSON."""
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    """Salvează lista de task-uri în fișier."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def add_task(title):
    deadline_str = input("Introdu un deadline (format: ZZ-LL-AAAA) sau lasă gol: ")
    deadline = None
    if deadline_str.strip():
        try:
            deadline = datetime.strptime(deadline_str, "%d-%m-%Y").strftime("%d-%m-%Y")
        except ValueError:
            print("Format invalid. Exemplu corect: 20-10-2025")
            return

    priority = ""
    while priority not in ["Low", "Medium", "High"]:
        priority = input("Setează prioritatea (Low / Medium / High): ").capitalize()
        if priority not in ["Low", "Medium", "High"]:
            print(" Prioritate invalidă! Alege Low, Medium sau High.")

    tasks = load_tasks()
    tasks.append({"title": title, "done": False, "deadline": deadline, "priority": priority})
    save_tasks(tasks)
    print(f" Task adăugat: {title} | Prioritate: {priority}")



def delete_task(index):
    """Șterge un task după index."""
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f" Task șters: {removed['title']}")
    else:
        print("Index invalid.")

def toggle_done(index):
    """Schimbă statusul unui task (done <-> not done)."""
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = not tasks[index - 1]["done"]
        save_tasks(tasks)
        status = "terminat" if tasks[index - 1]["done"] else "neterminat"
        print(f"Status schimbat: {tasks[index - 1]['title']} → {status}")
    else:
        print("Index invalid.")
def show_progress():
    """Afișează un mic progress bar cu procentul de taskuri terminate."""
    tasks = load_tasks()
    if not tasks:
        print("Niciun task adăugat încă.")
        return

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    percent = int((done / total) * 100)
    
    bar_length = 20
    filled = int(bar_length * percent / 100)
    bar = "█" * filled + "-" * (bar_length - filled)
    
    print(f"\n Progres: |{bar}| {percent}% ({done}/{total} finalizate)")

