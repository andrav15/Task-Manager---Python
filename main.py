from utils import add_task, load_tasks, delete_task, toggle_done, show_progress
from datetime import datetime
while True:
    show_progress()

    print("\n=== Task Manager ===")
    print("1. Adaugă task")
    print("2. Vezi lista cu task-uri")
    print("3. Ieși din meniu")
    print("4. Șterge task")
    print("5. Schimbă status Done/To-Do")
    
    opt = input("Alege o opțiune: ")
    
    if opt == "1":
        titlu = input("Scrie task-ul: ")
        add_task(titlu)
        
    elif opt == "2":
        tasks = load_tasks()
        if not tasks:
            print("Nu există task-uri.")
        else:
            today = datetime.now()
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            tasks = sorted(tasks, key=lambda x: priority_order.get(x.get("priority","Low")))
            for i, t in enumerate(tasks):
                status = "✔" if t["done"] else "X"
                deadline = t.get("deadline", None)
                if deadline:
                    deadline_date = datetime.strptime(deadline, "%d-%m-%Y")
                    days_left = (deadline_date - today).days
                    if t["done"]:
                        deadline_info = f"{deadline} (finalizat)"
                    elif days_left < 0:
                        deadline_info = f"{deadline} (termen depășit)"
                    else:
                        deadline_info = f"{deadline} ({days_left} zile rămase)"
                else:
                    deadline_info = "Fără deadline"
                priority = t.get("priority", "N/A")
                print(f"{i+1}. {t['title']} [{status}] - {deadline_info} | Prioritate: {priority}")

                
    elif opt == "3":
        print("La revedere!")
        break

    elif opt == "4":
        tasks = load_tasks()
        if not tasks:
            print("Nu există task-uri de șters.")
        else:
            for i, t in enumerate(tasks):
                print(f"{i+1}. {t['title']}")
            try:
                idx = int(input("Scrie numărul taskului de șters: "))
                delete_task(idx)
            except ValueError:
                print("Introdu un număr valid!")

    elif opt == "5":
        tasks = load_tasks()
        if not tasks:
            print("Nu există task-uri.")
        else:
            from datetime import datetime
            today = datetime.now()
            for i, t in enumerate(tasks):
                status = "✔" if t["done"] else "X"
                deadline = t.get("deadline", None)
                if deadline:
                    deadline_date = datetime.strptime(deadline, "%d-%m-%Y")
                    days_left = (deadline_date - today).days
                    if t["done"]:
                        deadline_info = f"{deadline} (finalizat)"
                    elif days_left < 0:
                        deadline_info = f"{deadline} (termen depășit)"
                    else:
                        deadline_info = f"{deadline} ({days_left} zile rămase)"
                else:
                    deadline_info = "Fără deadline"

            
                priority = t.get("priority", "N/A")
                print(f"{i+1}. {t['title']} [{status}] - {deadline_info} | Prioritate: {priority}")

            try:
                idx = int(input("Scrie numărul taskului pentru schimbare status: "))
                toggle_done(idx)
            except ValueError:
                print("Introdu un număr valid!")

    else:
        print("Opțiune invalidă. Alege 1, 2, 3, 4 sau 5.")
