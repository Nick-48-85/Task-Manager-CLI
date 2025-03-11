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
           due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
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
      "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "due_date": due_date_obj,
      "priority": priority,
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
    print("5. Add tags to task")
    print("6. Task statistics")
    print("7. Exit")
    return input("Enter your choice (1-7): ")

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

    filtered_tasks = []

    if filter_choice == "1":
        filtered_tasks = tasks
        print("\nShowing all tasks:")
    elif filter_choice == "2":
        filtered_tasks = [task for task in tasks if not task["completed"]]
        print("\nShowing only pending tasks:")
    elif filter_choice == "3":
        filtered_tasks = [task for task in tasks if task["completed"]]
        print("\nShowing only completed tasks:")
    elif filter_choice == "4":
        priority = input("Enter priority (low/medium/high): ").lower()
        filtered_tasks = [task for task in tasks if task["priority"] == priority]
        print(f"\nShowing tasks with priority {priority}:")
    elif filter_choice == "5":
        filtered_tasks = [task for task in tasks if task.get("due_date")]
        filtered_tasks.sort(key=lambda x: x["due_date"])
        print("\nShowing tasks by due date:")
    elif filter_choice == "6":
        tag = input("Enter tag: ")
        filtered_tasks = [task for task in tasks if tag in task.get("tags")]
        print(f"\nShowing tasks with tag {tag}:")
    else:
        print("Invalid choice. Showing all tasks.")
        filtered_tasks = tasks

    if filtered_tasks:
        print("\nSort by:")
        print("1. Creation date(default)")
        print("2. Due date")
        print("3. Priority")
        print("4. Title (alphabetical)")

        sort_choice = input("Enter your choice (1-4): ") or "1"

        if sort_choice == "1":
            filtered_tasks.sort(key=lambda x: x["created_at"])
        elif sort_choice == "2":
            filtered_tasks.sort(key=lambda x: x.get("due_date") or "9999-12-31")
        elif sort_choice == "3":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            filtered_tasks.sort(key=lambda x: priority_order.get(x["priority"], 1))
        elif sort_choice == "4":
            filtered_tasks.sort(key=lambda x: x["title"].lower())
           
        display_tasks(filtered_tasks)

    else: 
        print("No tasks found.")

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return  
    
    print("\nID | Status | Priority | Due Date | Title")
    print("-" * 60)

    for task in tasks:
        status = "✓" if task["completed"] else " "
        due_date = task.get("due_date", "None")
        priority_display = {"high": "HIGH", "medium": "MED", "low": "LOW"}.get(task["priority"], "MED")

        print(f"{task['id']:2} | [{status}] | {priority_display} | {due_date or 'None':11} | {task['title']}")

        if task.get("description"):
            print(f"    Description: {task['description']}")

        if task.get("tags", []):
            print(f"    Tags: {', '.join(task.get('tags', []))}")


    print("")

def add_tags_to_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return  
    
    list_tasks()

    try:
        task_id = int(input("Enter task ID: "))

        for task in tasks: 
            if task["id"] == task_id:
                current_tags = task.get("tags", [])
                print(f"Current tags: {', '.join(current_tags) if current_tags else 'None'}")

                new_tags = input("Enter tags separated by commas: ")
                tag_list = [tag.strip().lower() for tag in new_tags.split(",") if tag.strip()]

                for tag in tag_list:
                    if tag not in current_tags:
                        current_tags.append(tag)

                task["tags"] = current_tags
                save_tasks(tasks)
                print(f"Tags updated for task {task_id}: {', '.join(current_tags)}")
                return
            
        print(f"Task {task_id} not found.")
    except ValueError:
        print("Please enter a valid task ID.")

def show_statistics():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    pending_tasks = total_tasks - completed_tasks

    completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for task in tasks:
        priority = task.get("priority", "medium")
        priority_counts[priority] += 1

    tasks_with_due_date = sum(1 for task in tasks if task.get("due_date"))

    today = datetime.now().strftime("%Y-%m-%d")
    overdue_tasks = sum(1 for task in tasks if task.get("due_date") and task["due_date"] < today and not task["completed"])

    all_tags = []
    for task in tasks:
        all_tags.extend(task.get("tags", []))

    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print("\n==== Task Statistics ====")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks} ({completion_percentage:.1f}%)")
    print(f"Pending tasks: {pending_tasks} ({100 - completion_percentage:.1f}%)")
    print(f"\nTasks by priority:")
    for priority, count in priority_counts.items():
        percentage = (count / total_tasks) * 100 if total_tasks > 0 else 0
        print(f"  {priority.capitalize()}: {count} ({percentage:.1f}%)")
    
    print(f"\nTasks with due date: {tasks_with_due_date}")
    print(f"Overdue tasks: {overdue_tasks}")

    if tag_counts:
        print("\nMost used tags:")
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:5]:
            print(f"  {tag}: {count}")


def main():
    while True:
        choice = show_menu()
        
        if choice == "1":
            title = input("Title: ")
            description = input("Description: ")
            due_date = input("Due date (YYYY-MM-DD): ")
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
            filter_tasks()
        elif choice == "5":
            add_tags_to_task()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
         

