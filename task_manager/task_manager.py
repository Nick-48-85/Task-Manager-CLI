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


def add_task(title, description="", due_date=None, priority="medium"):
   tasks = load_tasks()

   due_date_obj = None
   if due_date:
       try:
           due_date_obj = datetime.strptime(due_date, %Y-%m-%d).strftime("%Y-%m-%d")
        except ValueError:
           print("Invalid due date format. Please use YYYY-MM-DD.")

valid_priorities = ["low", "medium", "high"]
if priority.lower() not in valid_priorities:
   print(f"Invalid priority. Please use one of: {', '.join(valid_priorities)}")
   priority = "medium"

   new_task = {
      "id" : len(tasks) + 1,
      "title": title,
      "description": description,    
      "completed": False,
      "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      "due_date": due_date_obj,
      "priority": priority
      "tags": []
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
    print("4. Filter tasks")
    print("5. Task statistics")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def filter_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    print("\n==== Filter Tasks ====")
    print("1. Show all tasks")
    print("2. Show only pending tasks")
    print("3. Show only completed tasks")
    print("4. Show tasks by priority")
    print("5. Show tasks by due date")
    print("6. Show tasks by tag")

    filter_choice = input("Enter your choice (1-6): ")

    filter_tasks = []

    if filter_choice == "1":
        filter_tasks = tasks
        print("\nShowing all tasks:")
    elif filter_choice == "2":
        filter_tasks = [task for task in tasks if not task["completed"]]
        print("\nShowing only pending tasks:")
    elif filter_choice == "3":
        filter_tasks = [task for task in tasks if task["completed"]]
        print("\nShowing only completed tasks:")
    elif filter_choice == "4":
        priority = input("Enter priority (low/medium/high): ").lower()
        filter_tasks = [task for task in tasks if task["priority"] == priority]
        print(f"\nShowing tasks with priority {priority}:")
    elif filter_choice == "5":
        filter_tasks = [task for task in tasks if task.get["due_date"]]
        filter_tasks.sort(key=lambda x: x["due_date"])
        print("\nShowing tasks by due date:")
    elif filter_choice == "6":
        tag = input("Enter tag: ")
        filter_tasks = [task for task in tasks if tag in task.get["tags"]]
        print(f"\nShowing tasks with tag {tag}:")
    else:
        print("Invalid choice. Showing all tasks.")
        filter_tasks = tasks

    if filter_tasks:
        print("\nSort by:")
        print("1. Creation date(default)")
        print("2. Due date")
        print("3. Priority")
        print("4. Title (aplphabetical)")

        sort_choice = input("Enter your choice (1-4): ") or "1"

        if sort_choice == "1":
            filter_tasks.sort(key=lambda x: x["created_at"])
        elif sort_choice == "2":
            filter_tasks.sort(key=lambda x: x.get("due_date") or "9999-12-31")
        elif sort_choice == "3":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            filter_tasks.sort(key=lambda x: priority_order.get[x["priority"], 1])
        elif sort_choice == "4":
            filter_tasks.sort(key=lambda x: x["title"].lower())
           
        display_tasks(filter_tasks)

    else: 
        print("No tasks found.")

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return  
    
    print("\nID | Status | Priority | Due Date | Title")
    print("-" * 50)

    for task in tasks:
        status = "✓" if task["completed"] else " "
        due_date = task.get("due_date", "None")
        priority_display = {"high": "HIGH", "medium": "MED", "low": "LOW"}.get(task["priority"], "MED")

        print(f"{task['id']:2} | [{status}] | {priority_display} | {due_date or 'None':11} | {task['title']}")

    print("")



def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            title = input("Title: ")
            description = input("Description: ")
            due_date = input("Due date (YYYY-MM-DD): ")
            print("Priority (low/medium/high): ")
            priority = input("Priority (low/medium/high): ")
            
            if not due_date:
                due_date = None

            add_task(title, description, due_date, priority)
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
         

