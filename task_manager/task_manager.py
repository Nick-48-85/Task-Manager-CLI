import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
          try:
             return json.load(file)
          except json.JSONDecodeError:
             return []
    return []
        
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def add_task(title, description=""):
   tasks = load_tasks()

   new_task = {
      "id" : len(tasks) + 1,
      "title": title,
      "description": description,    
      "completed": False,
      "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
   
   tasks.append(new_task)
   save_tasks(tasks)
   print(f"Task added: {title}")

def list_tasks():
    tasks = load_tasks()
       
    if not tasks:
        print("No tasks found.")
        return
       
    print("\nID | Status | Title")
    print("-" * 30)
   
    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"{task['id']:2} | [{status}] | {task['title']}")
           
def complete_task(task_id):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} completed.")
            return
    
    print(f"Task {task_id} not found.")

def show_menu():
    print("\n==== Task Manager ====")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete task")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(title, description)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            complete_task(task_id)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
         

